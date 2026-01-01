/**
 * Budgetary Impacts slide - shows 10-year budget window impacts.
 */

import { Box, Text, Stack } from '@mantine/core';
import Plot from 'react-plotly.js';
import { colors, spacing, typography } from '@/designTokens';

interface BudgetYearImpact {
  year: number;
  totalIncomeChange: number;
}

interface BudgetaryImpactsSlideProps {
  budgetWindowImpacts: BudgetYearImpact[];
  totalDeficitChange: number;
  baselineScenario: string;
}

export function BudgetaryImpactsSlide({
  budgetWindowImpacts,
  totalDeficitChange,
  baselineScenario,
}: BudgetaryImpactsSlideProps) {
  const impactWord = totalDeficitChange > 0 ? 'reduce' : 'increase';
  const impactAmount = Math.abs(totalDeficitChange) / 1e12;

  const years = budgetWindowImpacts.map((d) => d.year);
  const impacts = budgetWindowImpacts.map((d) => d.totalIncomeChange);
  const labels = budgetWindowImpacts.map((d) =>
    `$${Math.abs(d.totalIncomeChange / 1e9).toFixed(0)}B`
  );

  const data: Plotly.Data[] = [
    {
      x: years,
      y: impacts,
      type: 'bar',
      marker: { color: colors.primary[500] },
      text: labels,
      textposition: 'outside',
      hovertemplate: 'Year: %{x}<br>Impact: $%{y:,.0f}<extra></extra>',
    },
  ];

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: 'Year' },
      tickmode: 'linear',
      dtick: 1,
    },
    yaxis: {
      title: { text: 'Budgetary Impact (in billions)' },
      tickformat: '$,.0f',
    },
    margin: { t: 40, b: 80, l: 80, r: 60 },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    font: { family: 'Inter, sans-serif' },
  };

  if (totalDeficitChange === 0) {
    return (
      <Stack gap={spacing.lg}>
        <Text
          style={{
            fontSize: typography.fontSize.lg,
            color: colors.text.secondary,
          }}
        >
          Revise your policy using the left sidebar (policy) to see an impact
        </Text>
      </Stack>
    );
  }

  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        Your policy would {impactWord} the deficit by{' '}
        <Text
          component="span"
          style={{
            color: colors.primary[500],
            fontWeight: typography.fontWeight.bold,
          }}
        >
          ${impactAmount.toFixed(2)} trillion
        </Text>{' '}
        over the 10-year budget window, compared to {baselineScenario}
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <Plot
          data={data}
          layout={layout}
          useResizeHandler={true}
          style={{ width: '100%', height: '400px' }}
          config={{ responsive: true, displayModeBar: false }}
        />
      </Box>
    </Stack>
  );
}
