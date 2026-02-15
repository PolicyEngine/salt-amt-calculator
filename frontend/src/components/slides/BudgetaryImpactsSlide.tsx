/**
 * Budgetary Impacts slide - shows 10-year budget window impacts.
 */

import { Box, Text, Stack } from '@mantine/core';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from 'recharts';
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

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

export function BudgetaryImpactsSlide({
  budgetWindowImpacts,
  totalDeficitChange,
  baselineScenario,
}: BudgetaryImpactsSlideProps) {
  const impactWord = totalDeficitChange > 0 ? 'reduce' : 'increase';
  const impactAmount = Math.abs(totalDeficitChange) / 1e12;

  const data = budgetWindowImpacts.map((d) => ({
    year: d.year,
    impact: d.totalIncomeChange,
    label: `$${Math.abs(d.totalIncomeChange / 1e9).toFixed(0)}B`,
  }));

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
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data} margin={{ top: 30, right: 60, left: 80, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
            <XAxis
              dataKey="year"
              label={{ value: 'Year', position: 'insideBottom', offset: -10, style: { fontFamily: 'Inter, sans-serif', fontSize: 14 } }}
              style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
            />
            <YAxis
              tickFormatter={(v: number) => currencyFormatter.format(v)}
              label={{ value: 'Budgetary Impact (in billions)', angle: -90, position: 'insideLeft', dx: -20, style: { fontFamily: 'Inter, sans-serif', fontSize: 14, textAnchor: 'middle' } }}
              style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => [value != null ? currencyFormatter.format(Number(value)) : '', 'Impact']}
              labelFormatter={(label) => `Year: ${label}`}
              contentStyle={{ fontFamily: 'Inter, sans-serif' }}
            />
            <Bar dataKey="impact" fill={colors.primary[500]}>
              <LabelList dataKey="label" position="top" style={{ fontFamily: 'Inter, sans-serif', fontSize: 12 }} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Box>
    </Stack>
  );
}
