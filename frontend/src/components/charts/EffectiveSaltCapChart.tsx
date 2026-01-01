/**
 * Effective SALT Cap chart - shows effective SALT cap by income level.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';

interface EffectiveSaltCapChartProps {
  incomeValues: number[];
  effectiveSaltCap: number[];
  userIncome: number;
  userEffectiveSaltCap: number;
}

export function EffectiveSaltCapChart({
  incomeValues,
  effectiveSaltCap,
  userIncome,
  userEffectiveSaltCap,
}: EffectiveSaltCapChartProps) {
  const data: Plotly.Data[] = [
    // Effective SALT Cap line
    {
      x: incomeValues,
      y: effectiveSaltCap,
      type: 'scatter',
      mode: 'lines',
      name: 'Effective SALT Cap',
      line: { color: colors.primary[500], width: 1.5 },
      hovertemplate: 'Effective SALT Cap at<br>Income: $%{x:,.0f}<br>SALT: $%{y:,.0f}<extra></extra>',
    },
    // User marker
    {
      x: [userIncome],
      y: [userEffectiveSaltCap],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household<br>Income: $%{x:,.0f}<br>Effective SALT Cap: $%{y:,.0f}<extra></extra>',
    },
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
      title: { text: 'Effective SALT cap (2026)' },
      tickformat: '$,.0f',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      range: [0, 200000],
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
