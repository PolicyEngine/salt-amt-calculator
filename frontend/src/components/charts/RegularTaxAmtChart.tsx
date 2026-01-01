/**
 * Regular Tax and AMT chart - shows regular tax and AMT by SALT level.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface RegularTaxAmtChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userRegularTaxLaw: number;
  userRegularTaxPolicy: number;
  userAmtLaw: number;
  userAmtPolicy: number;
  showCurrentPolicy?: boolean;
}

export function RegularTaxAmtChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userRegularTaxLaw,
  userRegularTaxPolicy,
  userAmtLaw,
  userAmtPolicy,
  showCurrentPolicy = true,
}: RegularTaxAmtChartProps) {
  const data: Plotly.Data[] = [
    // Current Policy lines (in background, legendonly)
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.regularTax,
      type: 'scatter',
      mode: 'lines',
      name: 'Regular Tax (Current Policy)',
      line: { color: colors.gray[400], width: 2 },
      visible: showCurrentPolicy ? 'legendonly' : false,
      hovertemplate: 'SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>',
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.amt,
      type: 'scatter',
      mode: 'lines',
      name: 'AMT (Current Policy)',
      line: { color: colors.gray[400], width: 2, dash: 'dot' },
      visible: showCurrentPolicy ? 'legendonly' : false,
      hovertemplate: 'SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>',
    },
    // Current Law lines (in foreground)
    {
      x: currentLawData.axisValues,
      y: currentLawData.regularTax,
      type: 'scatter',
      mode: 'lines',
      name: 'Regular Tax (Current Law)',
      line: { color: colors.primary[500], width: 2 },
      hovertemplate: 'SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>',
    },
    {
      x: currentLawData.axisValues,
      y: currentLawData.amt,
      type: 'scatter',
      mode: 'lines',
      name: 'AMT (Current Law)',
      line: { color: colors.primary[500], width: 2, dash: 'dot' },
      hovertemplate: 'SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>',
    },
    // User markers - Current Law
    {
      x: [userSalt],
      y: [userRegularTaxLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household regular tax (Current Law)',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household (Current Law)<br>SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>',
    },
    {
      x: [userSalt],
      y: [userAmtLaw],
      type: 'scatter',
      mode: 'markers',
      name: 'Your household AMT (Current Law)',
      marker: { color: colors.primary[500], size: 10 },
      hovertemplate: 'Your household (Current Law)<br>SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>',
    },
    // User markers - Current Policy (legendonly)
    ...(showCurrentPolicy ? [
      {
        x: [userSalt],
        y: [userRegularTaxPolicy],
        type: 'scatter' as const,
        mode: 'markers' as const,
        name: 'Your household regular tax (Current Policy)',
        marker: { color: colors.gray[400], size: 10 },
        visible: 'legendonly' as const,
        hovertemplate: 'Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>',
      },
      {
        x: [userSalt],
        y: [userAmtPolicy],
        type: 'scatter' as const,
        mode: 'markers' as const,
        name: 'Your household AMT (Current Policy)',
        marker: { color: colors.gray[400], size: 10 },
        visible: 'legendonly' as const,
        hovertemplate: 'Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>',
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
      title: { text: 'Tax Amount (2026)' },
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
      x: 0.5,
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
