/**
 * Distributional Impacts slide - shows income distribution impacts.
 */

import { Box, Text, Stack, Card, SimpleGrid } from '@mantine/core';
import Plot from 'react-plotly.js';
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

export function DistributionalImpactsSlide({
  distributionData,
  pctBetterOff,
  pctWorseOff,
  avgImpactForAffected,
  baselineScenario,
}: DistributionalImpactsSlideProps) {
  const formatPercent = (value: number) => `${(value * 100).toFixed(1)}%`;
  const formatCurrency = (value: number) => `$${Math.abs(value).toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

  const deciles = distributionData.map((d) => d.decile);
  const impacts = distributionData.map((d) => d.avgImpact);

  const data: Plotly.Data[] = [
    {
      x: deciles,
      y: impacts,
      type: 'bar',
      marker: {
        color: impacts.map((v) => (v >= 0 ? colors.success : colors.error)),
      },
      hovertemplate: '%{x}<br>Average Impact: $%{y:,.0f}<extra></extra>',
    },
  ];

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: 'Income Decile' },
      tickangle: -45,
    },
    yaxis: {
      title: { text: 'Average Impact ($)' },
      tickformat: '$,.0f',
    },
    margin: { t: 40, b: 120, l: 80, r: 40 },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    font: { family: 'Inter, sans-serif' },
  };

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
        <Plot
          data={data}
          layout={layout}
          useResizeHandler={true}
          style={{ width: '100%', height: '400px' }}
          config={{ responsive: true, displayModeBar: false }}
        />
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
