/**
 * Base reusable line chart component for SALT/AMT analysis.
 * Handles common patterns: Current Law vs Current Policy, user markers.
 */

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceDot,
} from 'recharts';
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

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

const percentFormatter = (value: number) => `${(value * 100).toFixed(1)}%`;

function formatValue(value: number, format?: string): string {
  if (!format) return currencyFormatter.format(value);
  if (format.includes('%')) return percentFormatter(value);
  return currencyFormatter.format(value);
}

/**
 * Merge parallel x/y arrays from multiple lines into a single
 * array of {x, line0, line1, ...} objects for Recharts.
 */
function mergeLineData(lines: LineData[]): Record<string, number>[] {
  const dataMap = new Map<number, Record<string, number>>();

  lines.forEach((line, idx) => {
    if (line.visible === false) return;
    for (let i = 0; i < line.x.length; i++) {
      const xVal = line.x[i];
      if (!dataMap.has(xVal)) {
        dataMap.set(xVal, { x: xVal });
      }
      dataMap.get(xVal)![`line${idx}`] = line.y[i];
    }
  });

  return Array.from(dataMap.values()).sort((a, b) => a.x - b.x);
}

const STROKE_DASH: Record<string, string> = {
  solid: '',
  dot: '4 4',
  dash: '8 4',
};

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
  const data = mergeLineData(lines);

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 20, right: 40, left: 80, bottom: 60 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
        <XAxis
          dataKey="x"
          type="number"
          domain={xRange || ['auto', 'auto']}
          tickFormatter={(v: number) => formatValue(v, xTickFormat)}
          label={{ value: xAxisTitle, position: 'insideBottom', offset: -10, style: { fontFamily: 'Inter, sans-serif', fontSize: 14 } }}
          style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
        />
        <YAxis
          type="number"
          domain={yRange || ['auto', 'auto']}
          tickFormatter={(v: number) => formatValue(v, yTickFormat)}
          label={{ value: yAxisTitle, angle: -90, position: 'insideLeft', dx: -20, style: { fontFamily: 'Inter, sans-serif', fontSize: 14, textAnchor: 'middle' } }}
          style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
        />
        <Tooltip
          formatter={(value, name) => {
            if (value == null) return ['', name ?? ''];
            const lineIdx = parseInt(String(name).replace('line', ''), 10);
            const line = lines[lineIdx];
            return [formatValue(Number(value), yTickFormat), line?.name || String(name)];
          }}
          labelFormatter={(label) => `${xAxisTitle}: ${formatValue(Number(label), xTickFormat)}`}
          contentStyle={{ fontFamily: 'Inter, sans-serif' }}
        />
        <Legend
          formatter={(value: string) => {
            const lineIdx = parseInt(value.replace('line', ''), 10);
            return lines[lineIdx]?.name || value;
          }}
          wrapperStyle={{ fontFamily: 'Inter, sans-serif', paddingTop: '10px' }}
        />
        {lines.map((line, idx) => {
          if (line.visible === false) return null;
          return (
            <Line
              key={`line${idx}`}
              dataKey={`line${idx}`}
              name={`line${idx}`}
              stroke={line.color || colors.primary[500]}
              strokeWidth={2}
              strokeDasharray={STROKE_DASH[line.dash || 'solid'] || ''}
              dot={false}
              activeDot={{ r: 4 }}
              hide={line.visible === 'legendonly'}
            />
          );
        })}
        {markers.map((marker, idx) => (
          <ReferenceDot
            key={`marker${idx}`}
            x={marker.x}
            y={marker.y}
            r={6}
            fill={marker.color || colors.primary[500]}
            stroke="white"
            strokeWidth={2}
            label={{
              value: marker.name,
              position: 'top',
              offset: 10,
              style: { fontFamily: 'Inter, sans-serif', fontSize: 11, fill: marker.color || colors.primary[500] },
            }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
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
  const lineData: LineData[] = [
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

  const markerData: MarkerData[] = [
    {
      x: userX,
      y: userYLaw,
      name: 'You (Law)',
      color: colors.primary[500],
    },
    ...(showCurrentPolicy
      ? [
          {
            x: userX,
            y: userYPolicy,
            name: 'You (Policy)',
            color: colors.gray[400],
          },
        ]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lineData}
      markers={markerData}
      xAxisTitle={xAxisTitle}
      yAxisTitle={yAxisTitle}
      xRange={xRange}
      yTickFormat={yTickFormat}
    />
  );
}
