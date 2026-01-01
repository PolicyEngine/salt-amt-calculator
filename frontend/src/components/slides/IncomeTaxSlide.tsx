/**
 * Income Tax Comparison slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { IncomeTaxChart } from '@/components/charts/IncomeTaxChart';
import type { AxisResult } from '@/types';

interface IncomeTaxSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userTaxLaw: number;
  userTaxPolicy: number;
  effectiveSaltCapLaw: string;
  effectiveSaltCapPolicy: string;
  taxReductionLaw: number;
  taxReductionPolicy: number;
}

export function IncomeTaxSlide({
  currentLawData,
  currentPolicyData,
  userSalt,
  userTaxLaw,
  userTaxPolicy,
  effectiveSaltCapLaw,
  effectiveSaltCapPolicy,
  taxReductionLaw,
  taxReductionPolicy,
}: IncomeTaxSlideProps) {
  const formatCurrency = (value: number) => `$${value.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        You face an effective SALT cap of{' '}
        <Text component="span" style={{ color: colors.primary[500] }}>
          {effectiveSaltCapPolicy}
        </Text>{' '}
        under current policy and{' '}
        <Text component="span" style={{ color: colors.primary[500] }}>
          {effectiveSaltCapLaw}
        </Text>{' '}
        under current law.
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <IncomeTaxChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userSalt={userSalt}
          userTaxLaw={userTaxLaw}
          userTaxPolicy={userTaxPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        SALT could lower your taxes by up to{' '}
        <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.semibold }}>
          {formatCurrency(taxReductionLaw)}
        </Text>{' '}
        under current law and{' '}
        <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.semibold }}>
          {formatCurrency(taxReductionPolicy)}
        </Text>{' '}
        under current policy. Filers pay the greater of regular tax and AMT.
      </Text>
    </Stack>
  );
}
