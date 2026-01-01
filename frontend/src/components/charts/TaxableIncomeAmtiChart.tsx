/**
 * Taxable Income and AMTI chart - shows taxable income and AMTI by SALT level.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface TaxableIncomeAmtiChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userTaxableIncomeLaw: number;
  userTaxableIncomePolicy: number;
  userAmtiLaw: number;
  userAmtiPolicy: number;
  showCurrentPolicy?: boolean;
}

export function TaxableIncomeAmtiChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userTaxableIncomeLaw,
  userTaxableIncomePolicy,
  userAmtiLaw,
  userAmtiPolicy,
  showCurrentPolicy = true,
}: TaxableIncomeAmtiChartProps) {
  const data: Plotly.Data[] = [
    // Current Policy lines (in background, legendonly)
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.taxableIncome,
      type: 'scatter',
      mode: 'lines',
      name: 'Taxable Income (Current Policy)',
      line: { color: colors.gray[400], width: 2 },
      visible: showCurrentPolicy ? 'legendonly' : false,
      hovertemplate: 'SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>',
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.amtIncome,
      type: 'scatter',
      mode: 'lines',
      name: 'AMTI (Current Policy)',
      line: { color: colors.gray[400], width: 2, dash: 'dot' },
      visible: showCurrentPolicy ? 'legendonly' : false,
      hovertemplate: 'SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>',
    },
    // Current Law lines (in foreground)
    {
      x: currentLawData.axisValues,
      y: currentLawData.taxableIncome,
      type: 'scatter',
      mode: 'lines',
      name: 'Taxable Income (Current Law)',
      line: { color: colors.primary[500], width: 2 },
      hovertemplate: 'SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>',
    },
    {
      x: currentLawData.axisValues,
      y: currentLawData.amtIncome,
      type: 'scatter',
      mode: 'lines',
      name: 'AMTI (Current Law)',
      line: { color: colors.primary[500], width: 2, dash: 'dot' },
      hovertemplate: 'SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>',
    },
    // User markers - Current Law
    {
      x: [userSalt],
      y: [userTaxableIncomeLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household taxable income (Current Law)',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household (Current Law)<br>SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>',
    },
    {
      x: [userSalt],
      y: [userAmtiLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household AMTI (Current Law)',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household (Current Law)<br>SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>',
    },
    // User markers - Current Policy (legendonly)
    ...(showCurrentPolicy ? [
      {
        x: [userSalt],
        y: [userTaxableIncomePolicy],
        type: 'scatter' as const,
        mode: 'markers' as const,
        name: 'Your household taxable income (Current Policy)',
        marker: { color: colors.gray[400], size: 10 },
        visible: 'legendonly' as const,
        hovertemplate: 'Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>',
      },
      {
        x: [userSalt],
        y: [userAmtiPolicy],
        type: 'scatter' as const,
        mode: 'markers' as const,
        name: 'Your household AMTI (Current Policy)',
        marker: { color: colors.gray[400], size: 10 },
        visible: 'legendonly' as const,
        hovertemplate: 'Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>',
      },
    ] : []),
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
      title: { text: 'Taxable Income (2026)' },
      tickformat: '$,.0f',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
    },
    margin: { t: 40, b: 80, l: 80, r: 40 },
    hovermode: 'closest',
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    legend: {
      yanchor: 'bottom',
      y: 0.01,
      xanchor: 'right',
      x: 0.55,
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
