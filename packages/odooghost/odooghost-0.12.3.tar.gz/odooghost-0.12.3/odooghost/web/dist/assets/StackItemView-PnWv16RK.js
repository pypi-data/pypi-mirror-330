import{o as t,c as e,d as a,g as h,h as V,r as M,a as r,b as o,i as d,t as k,F as N,e as B,j as R,w as m,k as A,l as I,m as O,p as j,u as E,q as g,s as U,v,n as z,_ as Q,V as Z,f as K,x as q,R as D}from"./index-BMoHE36i.js";import{a as F}from"./stack-DmeHJWeA.js";import{V as L,_ as P}from"./VWarningAlert-Csp6mpqg.js";import{s as f}from"./constant-DWkFHeG6.js";function G(c,s){return t(),e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true","data-slot":"icon"},[a("path",{"fill-rule":"evenodd",d:"M12 2.25a.75.75 0 0 1 .75.75v11.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5a.75.75 0 1 1 1.06-1.06l3.22 3.22V3a.75.75 0 0 1 .75-.75Zm-9 13.5a.75.75 0 0 1 .75.75v2.25a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5V16.5a.75.75 0 0 1 1.5 0v2.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V16.5a.75.75 0 0 1 .75-.75Z","clip-rule":"evenodd"})])}function H(c,s){return t(),e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 20 20",fill:"currentColor","aria-hidden":"true","data-slot":"icon"},[a("path",{"fill-rule":"evenodd",d:"M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z","clip-rule":"evenodd"})])}function Y(c,s){return t(),e("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24","stroke-width":"1.5",stroke:"currentColor","aria-hidden":"true","data-slot":"icon"},[a("path",{"stroke-linecap":"round","stroke-linejoin":"round",d:"M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"})])}function J(c,s){return t(),e("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24","stroke-width":"1.5",stroke:"currentColor","aria-hidden":"true","data-slot":"icon"},[a("path",{"stroke-linecap":"round","stroke-linejoin":"round",d:"M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z"})])}function W(c,s){return t(),e("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24","stroke-width":"1.5",stroke:"currentColor","aria-hidden":"true","data-slot":"icon"},[a("path",{"stroke-linecap":"round","stroke-linejoin":"round",d:"M5.25 7.5A2.25 2.25 0 0 1 7.5 5.25h9a2.25 2.25 0 0 1 2.25 2.25v9a2.25 2.25 0 0 1-2.25 2.25h-9a2.25 2.25 0 0 1-2.25-2.25v-9Z"})])}const X=h`
  mutation startStack($name: String!) {
    startStack(name: $name) {
      ... on StartStackSuccess {
        name
      }
      ... on StartStackError {
        message
      }
    }
  }
`,tt=h`
  mutation stopStack($name: String!) {
    stopStack(name: $name) {
      ... on StopStackSuccess {
        name
      }
      ... on StopStackError {
        message
      }
    }
  }
`,et=h`
  mutation restartStack($name: String!) {
    restartStack(name: $name) {
      ... on RestartStackSuccess {
        name
      }
      ... on RestartStackError {
        message
      }
    }
  }
`,at={class:"flex items-center justify-between border-b border-black/10 pb-4"},st={class:"overflow-x-auto flex-1 flex items-center gap-6"},nt={key:0},rt={class:"hidden sm:block"},ot={role:"list",class:"flex items-center flex-none gap-x-6 text-sm font-semibold leading-6 text-neutral-400 sm:border-l sm:border-neutral-700 sm:pl-6 sm:leading-7"},ct={class:""},lt={__name:"VNav",props:{title:String,navigation:Object,hasBack:{type:Boolean,default:!0},backlink:[Object,String]},setup(c){const s=c,l=V(),p=()=>{s.backlink?l.push(s.backlink):l.go(-1)};return(_,x)=>{const n=M("router-link");return t(),e("nav",at,[a("div",st,[s.hasBack?(t(),e("div",nt,[a("button",{onClick:p,class:"flex items-center text-sm font-medium group"},[r(o(H),{class:"flex-shrink-0 h-5 w-5 text-neutral-400 group-hover:text-primary","aria-hidden":"true"})])])):d("",!0),a("h2",rt,k(s.title),1),a("ul",ot,[(t(!0),e(N,null,B(s.navigation,u=>(t(),e("li",{key:u.name},[r(n,{to:u.to,"exact-active-class":"!text-primary"},{default:m(()=>[A(k(u.name),1)]),_:2},1032,["to"])]))),128))])]),a("div",ct,[R(_.$slots,"default")])])}}},it={key:0,class:"py-20"},ut={key:1,class:"py-20 max-w-xl mx-auto"},dt={key:2},mt={class:"flex gap-x-2"},kt={class:"button-circle"},pt={class:"flex gap-x-2"},_t={class:"inline-flex items-center rounded-xl bg-gray-400/10 px-2 py-1 text-xs text-gray-400"},vt={key:3,class:"py-20 max-w-xl mx-auto"},St={__name:"StackItemView",setup(c){const s=I(),l=O({name:s.params.stackId});j(()=>s.params.stackId,i=>{i!==void 0&&(l.name=i)});const{result:p,loading:_,error:x}=E(F,l),n=g(()=>{var i;return((i=p.value)==null?void 0:i.stack)??null}),u=g(()=>[{name:"Overview",to:{name:"stackIndex",params:{stackId:l.name}}}]);U("stack",n);const{mutate:w}=v(X,{refetchQueries:["getStack"]}),S=()=>{w({name:n.value.name})},{mutate:b}=v(tt,{refetchQueries:["getStack"]}),y=()=>{b({name:n.value.name})},{mutate:$}=v(et,{refetchQueries:["getStack"]}),C=()=>{$({name:n.value.name})};return(i,ht)=>(t(),e("div",null,[o(_)?(t(),e("div",it,[r(L)])):o(x)?(t(),e("div",ut,[r(Q,{title:"Une erreur est survenue !",text:"Veuillez réessayer plus tard. Si le problème persiste, contactez votre administrateur."})])):n.value?(t(),e("div",dt,[r(lt,{title:l.name,navigation:u.value,backlink:{name:"stacks"}},{default:m(()=>[a("div",mt,[a("button",kt,[r(o(G),{class:"h-5 w-5"})]),n.value.state!="RUNNING"?(t(),e("button",{key:0,onClick:S,class:"button-circle bg-green-600",title:"Start"},[r(o(J),{class:"h-5 w-5"})])):d("",!0),n.value.state=="RUNNING"?(t(),e("button",{key:1,onClick:C,class:"button-circle bg-blue-400",title:"Restart"},[r(o(Y),{class:"h-5 w-5"})])):d("",!0),n.value.state!="STOPPED"?(t(),e("button",{key:2,onClick:y,class:"button-circle bg-red-400",title:"Stop"},[r(o(W),{class:"h-5 w-5"})])):d("",!0)])]),_:1},8,["title","navigation"]),a("div",pt,[a("span",{class:z(["inline-flex items-center rounded-xl 0 px-2 py-1 text-xs",o(f)[n.value.state].classes])},"State: "+k(o(f)[n.value.state].label),3),a("span",_t,"Network: "+k(n.value.networkMode),1)]),r(o(D),null,{default:m(({Component:T})=>[r(Z,null,{default:m(()=>[(t(),K(q(T)))]),_:2},1024)]),_:1})])):(t(),e("div",vt,[r(P,{title:"Aucun résultat !",text:"Si vous pensez que c'est une erreur, contactez votre administrateur."})]))]))}};export{St as default};
