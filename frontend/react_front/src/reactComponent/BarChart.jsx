import {useD3} from './visualization';
import React from 'react';
import * as d3 from 'd3';

/**
 * The d3 svg barchart
 * @param {array} data
 * @returns the barchart in html
 */
function BarChart({data}) {
  const ref = useD3(
    (svg) => {
      const height = 500;
      const width = 1000;
      const margin = { top: 20, right: 30, bottom: 30, left: 40 };
      const x = d3
        .scaleBand()
        .domain(data.map((s) => s.name))
        .rangeRound([margin.left, width - margin.right])
        .padding(0.1);
      const yScale = d3
        .scaleLinear()
        .domain([0, d3.max(data, (d) => d.rating)])
        .rangeRound([height - margin.bottom, margin.top]);
      const xAxis = (g) =>
        g.attr("transform", `translate(0,${height - margin.bottom})`).call(
          d3
            .axisBottom(x)
            .tickSizeOuter(0)
        );
      const yScaleAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .style("color", "steelblue")
          .call(d3.axisLeft(yScale).ticks(null, "s"))
          .call((g) => g.select(".domain").remove())
          .call((g) =>
            g
              .append("text")
              .attr("x", -margin.left)
              .attr("y", 10)
              .attr("fill", "currentColor")
              .attr("text-anchor", "start")
              .text(data.yScale)
          );
      svg.select(".y-axis").call(yScaleAxis);
      svg.select(".x-axis").call(xAxis);
      svg
        .select(".plot-area")
        .attr("fill", "steelblue")
        .selectAll(".bar")
        .data(data)
        .join("rect")
        .attr("class", "bar")
        .attr("x", (d) => x(d.name))
        .attr("width", x.bandwidth())
        .attr("y", (d) => yScale(d.rating))
        .attr("height", (d) => yScale(0) - yScale(d.rating));
    },
    [data.length]
  );

  return (
    <svg
      ref={ref}
      style={{
        height: 500,
        width: "100%",
        marginRight: "0px",
        marginLeft: "0px",
      }}
    >
      <g className="plot-area" />
      <g className="x-axis" />
      <g className="y-axis" />
    </svg>
  );
}

export default BarChart;