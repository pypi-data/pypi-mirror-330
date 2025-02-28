import { p as parser$1, f as flowDb } from "./flowDb-d35e309a-BgotH_8d.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-7383a064-C_1ij5IS.js";
import { t as setConfig } from "./index-DV1UwMfd.js";
import "./graph-DzGuEeOg.js";
import "./layout-IYnsxoHZ.js";
import "./index-8fae9850-DLIfboKj.js";
import "./clone-B9IT39Be.js";
import "./edges-d417c7a0-CvzUtFG_.js";
import "./createText-423428c9--oDTv9xx.js";
import "./line-CkUaj3lP.js";
import "./array-DgktLKBx.js";
import "./path-Cp2qmpkd.js";
import "./channel-DMHQvgiM.js";
const diagram = {
  parser: parser$1,
  db: flowDb,
  renderer: flowRendererV2,
  styles: flowStyles,
  init: (cnf) => {
    if (!cnf.flowchart) {
      cnf.flowchart = {};
    }
    cnf.flowchart.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    setConfig({ flowchart: { arrowMarkerAbsolute: cnf.arrowMarkerAbsolute } });
    flowRendererV2.setConf(cnf.flowchart);
    flowDb.clear();
    flowDb.setGen("gen-2");
  }
};
export {
  diagram
};
//# sourceMappingURL=flowDiagram-v2-49332944-DChj2_Km.js.map
