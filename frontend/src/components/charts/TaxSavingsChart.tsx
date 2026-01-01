/**
 * Tax Savings chart - shows tax savings by income level.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';

interface TaxSavingsChartProps {
  incomeValues: number[];
  taxSavings: number[];
  userIncome: number;
  userTaxSavings: number;
}

export function TaxSavingsChart({
  incomeValues,
  taxSavings,
  userIncome,
  userTaxSavings,
}: TaxSavingsChartProps) {
  const data: Plotly.Data[] = [
    // Tax Savings line
    {
      x: incomeValues,
      y: taxSavings,
      type: 'scatter',
      mode: 'lines',
      name: 'Tax Savings',
      line: { color: colors.primary[500], width: 1.5 },
      hovertemplate: 'Income: $%{x:,.0f}<br>Tax Savings: $%{y:,.0f}<extra></extra>',
    },
    // User marker
    {
      x: [userIncome],
      y: [userTaxSavings],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household<br>Income: $%{x:,.0f}<br>Tax Savings: $%{y:,.0f}<extra></extra>',
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
      title: { text: 'Tax Savings' },
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
