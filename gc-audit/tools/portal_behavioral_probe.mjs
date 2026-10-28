/** Local, synthetic HTTP and store observations. No OAuth callback or external fetch. */
import assert from "node:assert/strict";
import {spawn} from "node:child_process";
import {mkdtempSync,rmSync} from "node:fs";
import {createServer} from "node:net";
import {tmpdir} from "node:os";
import {join,resolve} from "node:path";
import {pathToFileURL} from "node:url";
import {DatabaseSync} from "node:sqlite";

const root=resolve(process.argv[2]??"");
const imported=async path=>import(pathToFileURL(join(root,path)).href);
const {SQLiteAuthStore}=await imported("src/auth/sqlite-auth-store.mjs");
const {EditorialStore}=await imported("src/storage/editorial-store.mjs");
const temp=mkdtempSync(join(tmpdir(),"gc-audit-portal-"));
const freePort=()=>new Promise((ok,fail)=>{const server=createServer();server.once("error",fail);server.listen(0,"127.0.0.1",()=>{const port=server.address().port;server.close(()=>ok(port))})});
const port=await freePort(),origin=`http://127.0.0.1:${port}`;
const env={PATH:process.env.PATH??"",LOCALAPPDATA:temp,PORT:String(port),
  GITHUB_CLIENT_ID:"synthetic-client",GITHUB_CLIENT_SECRET:"synthetic-secret",PORTAL_OWNER_GITHUB_ID:"100"};
for(const key of ["SYSTEMROOT","WINDIR","COMSPEC","PATHEXT"])if(process.env[key])env[key]=process.env[key];
const child=spawn(process.execPath,[join(root,"src/local-server.mjs")],{cwd:root,env,stdio:["ignore","pipe","pipe"]});
let serverError="";child.stderr.on("data",chunk=>{serverError+=chunk.toString("utf8")});
const observations=[];
function record(id,method,expected,actual,controls){assert.equal(actual,expected,id);observations.push({id,method,expected,observed:actual,control_ids:controls,verification:"LOCAL_ASSERTION"})}
const request=(path,options={})=>fetch(origin+path,{redirect:"manual",signal:AbortSignal.timeout(3000),...options});
const post=(path,cookie,csrf,extra={})=>request(path,{method:"POST",headers:{cookie,origin,"content-type":"application/json",...(csrf?{"x-csrf-token":csrf}:{}),...extra},body:JSON.stringify({releaseId:"unconfigured"})});
try{
  let ready=false;
  for(let i=0;i<60;i++){
    if(child.exitCode!==null)throw new Error(`portal server exited: ${serverError}`);
    try{const response=await request("/health");if(response.status===200){ready=true;break}}catch{}
    await new Promise(ok=>setTimeout(ok,50));
  }
  if(!ready)throw new Error(`portal server did not become ready: ${serverError}`);
  record("http.anonymous.dashboard","HTTP GET /api/dashboard",401,(await request("/api/dashboard")).status,["ZTA-01.02","ZTA-02.01","ZTA-06.01"]);
  record("http.anonymous.import","HTTP POST /api/observatory/import",401,(await post("/api/observatory/import","",null)).status,["ZTA-02.01","ZTA-06.01"]);
  const db=new SQLiteAuthStore(join(temp,"GovernanceCommons","Portal","portal.sqlite"));
  let ownerToken,reviewerToken;
  try{
    db.db.prepare("INSERT INTO members(workspace_id,github_subject,role,disabled) VALUES('gc','200','reviewer',0)").run();
    db.db.prepare("INSERT INTO members(workspace_id,github_subject,role,disabled) VALUES('gc','201','reviewer',1)").run();
    ownerToken=db.issueSession({githubSubject:"100"});
    reviewerToken=db.issueSession({githubSubject:"200"});
    const disabledToken=db.issueSession({githubSubject:"201"});
    record("http.owner.dashboard","HTTP GET /api/dashboard",200,(await request("/api/dashboard",{headers:{cookie:`gc_session=${ownerToken}`}})).status,["ZTA-01.02","ZTA-02.01"]);
    record("http.disabled-membership.dashboard","HTTP GET /api/dashboard",401,(await request("/api/dashboard",{headers:{cookie:`gc_session=${disabledToken}`}})).status,["ZTA-02.01","ZTA-10.01"]);
    const ownerCookie=`gc_session=${ownerToken}`;
    record("http.import.missing-csrf","HTTP POST /api/observatory/import",403,(await post("/api/observatory/import",ownerCookie,null)).status,["ZTA-05.01","ZTA-06.01"]);
    const ownerSession=await request("/api/session",{headers:{cookie:ownerCookie}});
    assert.equal(ownerSession.status,200);
    const ownerCsrf=(await ownerSession.json()).csrfToken;
    record("http.import.wrong-origin","HTTP POST /api/observatory/import",403,(await post("/api/observatory/import",ownerCookie,ownerCsrf,{origin:"http://invalid.example"})).status,["ZTA-06.01"]);
    const reviewerCookie=`gc_session=${reviewerToken}`;
    const reviewerSession=await request("/api/session",{headers:{cookie:reviewerCookie}});
    assert.equal(reviewerSession.status,200);
    const reviewerCsrf=(await reviewerSession.json()).csrfToken;
    record("http.reviewer.import-denied","HTTP POST /api/observatory/import",403,(await post("/api/observatory/import",reviewerCookie,reviewerCsrf)).status,["ZTA-02.01","ZTA-10.01"]);
    db.revokeSession(ownerToken);
    record("http.revoked-session.dashboard","HTTP GET /api/dashboard",401,(await request("/api/dashboard",{headers:{cookie:ownerCookie}})).status,["ZTA-01.02","ZTA-02.02","ZTA-10.01"]);
  }finally{db.close()}

  const memory=new DatabaseSync(":memory:");
  try{
    let sequence=0;
    const store=new EditorialStore({db:memory,now:()=>"2026-10-28T00:00:00Z",id:()=>`pilot-${++sequence}`});
    memory.prepare("INSERT INTO workspaces(id,name) VALUES('gc','Synthetic')").run();
    for(const [subject,role] of [["300","contributor"],["400","editor"],["100","owner"]])
      memory.prepare("INSERT INTO members(workspace_id,github_subject,role,disabled) VALUES('gc',?,?,0)").run(subject,role);
    memory.prepare(`INSERT INTO observatory_publications(workspace_id,publication_id,schema_version,generated_at,records_url,records_sha256,
      manifest_sha256,record_count,approved_by,approval_record_id,source_commit,methodology_version,imported_by,imported_at)
      VALUES('gc','source-1','v1','2026-10-28','https://example.invalid/records',?,?,1,'owner','approval-1',?,'v1','100','2026-10-28')`)
      .run("a".repeat(64),"b".repeat(64),"c".repeat(40));
    memory.prepare(`INSERT INTO editorial_candidates(workspace_id,id,publication_id,source_record_id,subject_id,subject_version,title,summary,
      source_url,evidence_class,captured_at,limitations,status,created_at) VALUES('gc','candidate-1','source-1','record-1','subject-1','v1',
      'Synthetic candidate','Synthetic summary','https://example.invalid/source','documentation','2026-10-28','Synthetic only','unverified_candidate','2026-10-28')`).run();
    const draft=store.createDraftFromCandidate({workspaceId:"gc",actorSubject:"300",candidateId:"candidate-1",title:"Synthetic draft",content:"Local fixture"});
    store.submitForReview({workspaceId:"gc",actorSubject:"300",submissionId:draft.submissionId});
    const reviewArgs={workspaceId:"gc",submissionId:draft.submissionId,verdict:"verified",evidenceReference:"synthetic-review"};
    assert.throws(()=>store.recordReview({...reviewArgs,actorSubject:"300"}),/review denied|independent review required/);
    observations.push({id:"store.author-cannot-review",method:"EditorialStore.recordReview",expected:"DENIED",observed:"DENIED",control_ids:["ZTA-02.01","ZTA-10.01"],verification:"LOCAL_ASSERTION"});
    store.recordReview({...reviewArgs,actorSubject:"400"});
    const decisionArgs={workspaceId:"gc",submissionId:draft.submissionId,decision:"approved",rationale:"Synthetic decision"};
    assert.throws(()=>store.recordDecision({...decisionArgs,actorSubject:"400"}),/independent approval required/);
    observations.push({id:"store.reviewer-cannot-approve",method:"EditorialStore.recordDecision",expected:"DENIED",observed:"DENIED",control_ids:["ZTA-02.01","ZTA-10.01"],verification:"LOCAL_ASSERTION"});
    const approved=store.recordDecision({...decisionArgs,actorSubject:"100"});
    record("store.independent-approver","EditorialStore.recordDecision","approved",approved.status,["ZTA-02.01"]);
  }finally{memory.close()}
  process.stdout.write(JSON.stringify({schema:"gc-audit.portal-observations.v1",environment:"synthetic isolated LOCALAPPDATA and in-memory editorial SQLite",observations})+"\n");
}finally{
  child.kill("SIGTERM");
  await Promise.race([new Promise(ok=>child.once("exit",ok)),new Promise(ok=>setTimeout(ok,1500))]);
  if(child.exitCode===null)child.kill("SIGKILL");
  rmSync(temp,{recursive:true,force:true});
}
