/**
 * Distributional Impacts slide - shows income distribution impacts.
 */

import { Box, Text, Stack, Card, SimpleGrid } from '@mantine/core';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { colors, spacing, typography } from '@/designTokens';

interface DistributionData {
  decile: string;
  avgImpact: number;
  pctBetterOff: number;
  pctWorseOff: number;
}

interface DistributionalImpactsSlideProps {
  distributionData: DistributionData[];
  pctBetterOff: number;
  pctWorseOff: number;
  avgImpactForAffected: number;
  baselineScenario: string;
}

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

export function DistributionalImpactsSlide({
  distributionData,
  pctBetterOff,
  pctWorseOff,
  avgImpactForAffected,
  baselineScenario,
}: DistributionalImpactsSlideProps) {
  const formatPercent = (value: number) => `${(value * 100).toFixed(1)}%`;
  const formatCurrency = (value: number) => `$${Math.abs(value).toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

  const data = distributionData.map((d) => ({
    decile: d.decile,
    avgImpact: d.avgImpact,
  }));

  return (
    <Stack gap={spacing.lg}>
      <SimpleGrid cols={3} spacing="md">
        <Card
          style={{
            padding: spacing.md,
            textAlign: 'center',
            background: colors.background.secondary,
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.sm,
              color: colors.text.secondary,
            }}
          >
            Better Off
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize['2xl'],
              fontWeight: typography.fontWeight.bold,
              color: colors.success,
            }}
          >
            {formatPercent(pctBetterOff)}
          </Text>
        </Card>

        <Card
          style={{
            padding: spacing.md,
            textAlign: 'center',
            background: colors.background.secondary,
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.sm,
              color: colors.text.secondary,
            }}
          >
            Worse Off
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize['2xl'],
              fontWeight: typography.fontWeight.bold,
              color: colors.error,
            }}
          >
            {formatPercent(pctWorseOff)}
          </Text>
        </Card>

        <Card
          style={{
            padding: spacing.md,
            textAlign: 'center',
            background: colors.background.secondary,
          }}
        >
          <Text
            style={{
              fontSize: typography.fontSize.sm,
              color: colors.text.secondary,
            }}
          >
            Avg. Impact (if affected)
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize['2xl'],
              fontWeight: typography.fontWeight.bold,
              color: avgImpactForAffected >= 0 ? colors.success : colors.error,
            }}
          >
            {avgImpactForAffected >= 0 ? '+' : '-'}{formatCurrency(avgImpactForAffected)}
          </Text>
        </Card>
      </SimpleGrid>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data} margin={{ top: 20, right: 40, left: 80, bottom: 80 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
            <XAxis
              dataKey="decile"
              angle={-45}
              textAnchor="end"
              label={{ value: 'Income Decile', position: 'insideBottom', offset: -20, style: { fontFamily: 'Inter, sans-serif', fontSize: 14 } }}
              style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
            />
            <YAxis
              tickFormatter={(v: number) => currencyFormatter.format(v)}
              label={{ value: 'Average Impact ($)', angle: -90, position: 'insideLeft', dx: -20, style: { fontFamily: 'Inter, sans-serif', fontSize: 14, textAnchor: 'middle' } }}
              style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => [value != null ? currencyFormatter.format(Number(value)) : '', 'Average Impact']}
              contentStyle={{ fontFamily: 'Inter, sans-serif' }}
            />
            <Bar dataKey="avgImpact">
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.avgImpact >= 0 ? colors.success : colors.error}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
          textAlign: 'center',
        }}
      >
        Distributional impacts compared to {baselineScenario}
      </Text>
    </Stack>
  );
}
