/**
 * Gap chart - shows gap between Regular Tax and AMT by income level.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface GapChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userIncome: number;
  userGapLaw: number;
  userGapPolicy: number;
  showCurrentPolicy?: boolean;
}

export function GapChart({
  currentLawData,
  currentPolicyData,
  userIncome,
  userGapLaw,
  userGapPolicy,
  showCurrentPolicy = true,
}: GapChartProps) {
  const data: Plotly.Data[] = [
    // Current Law line
    {
      x: currentLawData.axisValues,
      y: currentLawData.gap || [],
      type: 'scatter',
      mode: 'lines',
      name: 'Current Law',
      line: { color: colors.primary[500], width: 2 },
      hovertemplate: 'Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>',
    },
    // Current Policy line
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.gap || [],
      type: 'scatter',
      mode: 'lines',
      name: 'Current Policy',
      line: { color: colors.gray[400], width: 2, dash: 'dash' },
      visible: showCurrentPolicy ? 'legendonly' : false,
      hovertemplate: 'Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>',
    },
    // User marker - Current Law
    {
      x: [userIncome],
      y: [userGapLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household (Current Law)',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household (Current Law)<br>Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>',
    },
    // User marker - Current Policy
    ...(showCurrentPolicy ? [{
      x: [userIncome],
      y: [userGapPolicy],
      type: 'scatter' as const,
      mode: 'markers' as const,
      name: 'Your household (Current Policy)',
      marker: { color: colors.gray[400], size: 10 },
      visible: 'legendonly' as const,
      hovertemplate: 'Your household (Current Policy)<br>Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>',
    }] : []),
  ];

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: 'Wages and salaries' },
      tickformat: '$,.0f',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      range: [0, 1000000],
    },
    yaxis: {
      title: { text: 'Gap between Regular Tax and AMT (assuming no SALT)' },
      tickformat: '$,.0f',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
    },
    margin: { t: 40, b: 80, l: 80, r: 40 },
    hovermode: 'closest',
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    legend: {
      yanchor: 'top',
      y: 0.99,
      xanchor: 'right',
      x: 0.99,
    },
    font: { family: 'Inter, sans-serif' },
  };

  return (
    <Plot
      data={data}
      layout={layout}
      useResizeHandler={true}
      style={{ width: '100%', height: '400px' }}
      config={{ responsive: true, displayModeBar: false }}
    />
  );
}
