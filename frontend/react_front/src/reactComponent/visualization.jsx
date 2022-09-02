import React from 'react';
import * as d3 from 'd3';

/**
 * d3 renderer
 * @param dependencies this is used  to check if we need to render the graph
 * @param renderChartFn the render function
 * @return the ref of the graph
 */
export const useD3 = (renderChartFn, dependencies) => {
    const ref = React.useRef();

    React.useEffect(() => {
        renderChartFn(d3.select(ref.current));
        return () => {};
      }, dependencies);
    return ref;
}