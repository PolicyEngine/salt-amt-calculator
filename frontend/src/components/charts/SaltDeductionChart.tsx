/**
 * SALT Deduction comparison chart component.
 * Shows SALT deduction vs reported SALT for Current Law and Current Policy.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';

interface ChartData {
  axisValues: number[];
  saltDeduction: number[];
}

interface SaltDeductionChartProps {
  currentLawData: ChartData;
  currentPolicyData: ChartData;
  userSalt: number;
  userDeductionLaw: number;
  userDeductionPolicy: number;
  showCurrentPolicy?: boolean;
}

export function SaltDeductionChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userDeductionLaw,
  userDeductionPolicy,
  showCurrentPolicy = true,
}: SaltDeductionChartProps) {
  const data: Plotly.Data[] = [
    // Current Law line
    {
      x: currentLawData.axisValues,
      y: currentLawData.saltDeduction,
      type: 'scatter',
      mode: 'lines',
      name: 'Current Law',
      line: { color: colors.primary[500], width: 2 },
      hovertemplate: 'SALT: $%{x:,.0f}<br>Deduction: $%{y:,.0f}<extra></extra>',
    },
    // Current Policy line
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.saltDeduction,
      type: 'scatter',
      mode: 'lines',
      name: 'Current Policy',
      line: { color: colors.text.muted, width: 2, dash: 'solid' },
      hovertemplate: 'SALT: $%{x:,.0f}<br>Deduction: $%{y:,.0f}<extra></extra>',
      visible: showCurrentPolicy ? true : 'legendonly',
    },
    // User's household marker (Current Law)
    {
      x: [userSalt],
      y: [userDeductionLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household (Current Law)',
      marker: { color: colors.primary[500], size: 10, symbol: 'circle' },
      hovertemplate: 'Your household<br>SALT: $%{x:,.0f}<br>Deduction: $%{y:,.0f}<extra></extra>',
    },
    // User's household marker (Current Policy)
    ...(showCurrentPolicy
      ? [
          {
            x: [userSalt],
            y: [userDeductionPolicy],
            type: 'scatter' as const,
            mode: 'markers' as const,
            name: 'Your household (Current Policy)',
            marker: { color: colors.text.muted, size: 10, symbol: 'circle' as const },
            hovertemplate: 'Your household<br>SALT: $%{x:,.0f}<br>Deduction: $%{y:,.0f}<extra></extra>',
          },
        ]
      : []),
  ];

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: 'Reported SALT' },
      tickformat: '$,.0f',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      range: [0, 100000],
    },
    yaxis: {
      title: { text: 'SALT Deduction (2026)' },
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
    font: {
      family: 'Inter, sans-serif',
    },
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
