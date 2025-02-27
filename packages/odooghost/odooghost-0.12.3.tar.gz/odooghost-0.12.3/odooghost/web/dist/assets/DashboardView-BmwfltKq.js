import{g as i,u as c,c as l,a as e,w as u,b as s,o as _,d as a}from"./index-BMoHE36i.js";import{_ as d}from"./VContainers-0Re2gZqH.js";import{_ as m,a as f}from"./VHeader-B49mfAkQ.js";import{_ as o}from"./VStat-BEe8tvTO.js";import"./VWarningAlert-Csp6mpqg.js";const g=i`
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
`,p={class:"mx-auto max-w-7xl"},h={class:"grid grid-cols-1 gap-4 sm:grid-cols-3"},k=a("h3",null,"Running Containers",-1),$={__name:"DashboardView",setup(v){const{result:t,loading:n,error:r}=c(g);return(x,D)=>(_(),l("div",null,[e(f,{title:"Dashboard"}),e(m,{loading:s(n),error:s(r),result:s(t),"result-key":"version"},{default:u(()=>[a("section",null,[a("div",p,[a("div",h,[e(o,{name:"Odooghost version",stat:s(t).version},null,8,["stat"]),e(o,{name:"Docker version",stat:s(t).dockerVersion},null,8,["stat"]),e(o,{name:"Stacks count",stat:s(t).stackCount},null,8,["stat"])])])]),a("section",null,[k,e(d,{containers:s(t).containers},null,8,["containers"])])]),_:1},8,["loading","error","result"])]))}};export{$ as default};
