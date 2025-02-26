import{g as l,u as c,c as u,a as e,w as d,b as s,o as m,d as a}from"./index-D6C1uBe7.js";import{_}from"./VContainers-CE1MB-87.js";import{_ as f,a as g}from"./VHeader-DqL5pwie.js";import{_ as o}from"./VStat-By_bJy0T.js";import"./VWarningAlert-z4J3XwkV.js";const p=l`
  query getDashboard {
    version
    dockerVersion
    stackCount
    containers(stopped: false) {
      id
      name
      image
      service
      state
    }
  }
`,k={class:"mx-auto max-w-7xl"},v={class:"grid grid-cols-1 gap-4 sm:grid-cols-3"},C={__name:"DashboardView",setup(h){const{result:t,loading:r,error:i}=c(p);return(x,n)=>(m(),u("div",null,[e(f,{title:"Dashboard"}),e(g,{loading:s(r),error:s(i),result:s(t),"result-key":"version"},{default:d(()=>[a("section",null,[a("div",k,[a("div",v,[e(o,{name:"Odooghost version",stat:s(t).version},null,8,["stat"]),e(o,{name:"Docker version",stat:s(t).dockerVersion},null,8,["stat"]),e(o,{name:"Stacks count",stat:s(t).stackCount},null,8,["stat"])])])]),a("section",null,[n[0]||(n[0]=a("h3",null,"Running Containers",-1)),e(_,{containers:s(t).containers},null,8,["containers"])])]),_:1},8,["loading","error","result"])]))}};export{C as default};
