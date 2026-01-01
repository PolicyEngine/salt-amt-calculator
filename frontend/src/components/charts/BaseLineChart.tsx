/**
 * Base reusable line chart component for SALT/AMT analysis.
 * Handles common patterns: Current Law vs Current Policy, user markers.
 */

import Plot from 'react-plotly.js';
import { colors } from '@/designTokens';

interface LineData {
  x: number[];
  y: number[];
  name: string;
  color?: string;
  dash?: 'solid' | 'dot' | 'dash';
  visible?: boolean | 'legendonly';
}

interface MarkerData {
  x: number;
  y: number;
  name: string;
  color?: string;
}

interface BaseLineChartProps {
  lines: LineData[];
  markers?: MarkerData[];
  xAxisTitle: string;
  yAxisTitle: string;
  xRange?: [number, number];
  yRange?: [number, number];
  xTickFormat?: string;
  yTickFormat?: string;
  height?: number;
}

export function BaseLineChart({
  lines,
  markers = [],
  xAxisTitle,
  yAxisTitle,
  xRange,
  yRange,
  xTickFormat = '$,.0f',
  yTickFormat = '$,.0f',
  height = 400,
}: BaseLineChartProps) {
  const data: Plotly.Data[] = [
    // Lines
    ...lines.map((line) => ({
      x: line.x,
      y: line.y,
      type: 'scatter' as const,
      mode: 'lines' as const,
      name: line.name,
      line: {
        color: line.color || colors.primary[500],
        width: 2,
        dash: line.dash || 'solid',
      },
      visible: line.visible ?? true,
      hovertemplate: `${xAxisTitle}: %{x:${xTickFormat}}<br>${yAxisTitle}: %{y:${yTickFormat}}<extra></extra>`,
    })),
    // Markers
    ...markers.map((marker) => ({
      x: [marker.x],
      y: [marker.y],
      type: 'scatter' as const,
      mode: 'markers' as const,
      name: marker.name,
      marker: {
        color: marker.color || colors.primary[500],
        size: 10,
        symbol: 'circle' as const,
      },
      hovertemplate: `${marker.name}<br>${xAxisTitle}: %{x:${xTickFormat}}<br>${yAxisTitle}: %{y:${yTickFormat}}<extra></extra>`,
    })),
  ];

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: xAxisTitle },
      tickformat: xTickFormat,
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      range: xRange,
    },
    yaxis: {
      title: { text: yAxisTitle },
      tickformat: yTickFormat,
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      range: yRange,
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
      style={{ width: '100%', height: `${height}px` }}
      config={{ responsive: true, displayModeBar: false }}
    />
  );
}

// Convenience component for Current Law vs Current Policy charts
interface ComparisonChartProps {
  currentLawX: number[];
  currentLawY: number[];
  currentPolicyX: number[];
  currentPolicyY: number[];
  userX: number;
  userYLaw: number;
  userYPolicy: number;
  xAxisTitle: string;
  yAxisTitle: string;
  showCurrentPolicy?: boolean;
  xRange?: [number, number];
  yTickFormat?: string;
}

export function ComparisonChart({
  currentLawX,
  currentLawY,
  currentPolicyX,
  currentPolicyY,
  userX,
  userYLaw,
  userYPolicy,
  xAxisTitle,
  yAxisTitle,
  showCurrentPolicy = true,
  xRange,
  yTickFormat = '$,.0f',
}: ComparisonChartProps) {
  const lines: LineData[] = [
    {
      x: currentLawX,
      y: currentLawY,
      name: 'Current Law',
      color: colors.primary[500],
    },
    {
      x: currentPolicyX,
      y: currentPolicyY,
      name: 'Current Policy',
      color: colors.gray[400],
      visible: showCurrentPolicy ? true : 'legendonly',
    },
  ];

  const markers: MarkerData[] = [
    {
      x: userX,
      y: userYLaw,
      name: 'Your household (Current Law)',
      color: colors.primary[500],
    },
    ...(showCurrentPolicy
      ? [
          {
            x: userX,
            y: userYPolicy,
            name: 'Your household (Current Policy)',
            color: colors.gray[400],
          },
        ]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle={xAxisTitle}
      yAxisTitle={yAxisTitle}
      xRange={xRange}
      yTickFormat={yTickFormat}
    />
  );
}
