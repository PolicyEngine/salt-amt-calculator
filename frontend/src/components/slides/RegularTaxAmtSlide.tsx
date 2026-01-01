/**
 * Regular Tax and AMT Comparison slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { RegularTaxAmtChart } from '@/components/charts/RegularTaxAmtChart';
import type { AxisResult } from '@/types';

interface RegularTaxAmtSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userRegularTaxLaw: number;
  userRegularTaxPolicy: number;
  userAmtLaw: number;
  userAmtPolicy: number;
  effectiveSaltCapDisplay: string;
}

export function RegularTaxAmtSlide({
  currentLawData,
  currentPolicyData,
  userSalt,
  userRegularTaxLaw,
  userRegularTaxPolicy,
  userAmtLaw,
  userAmtPolicy,
  effectiveSaltCapDisplay,
}: RegularTaxAmtSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        With{' '}
        <Text component="span" style={{ color: colors.primary[500] }}>
          {effectiveSaltCapDisplay}
        </Text>{' '}
        in SALT, under current law AMT equals regular tax
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <RegularTaxAmtChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userSalt={userSalt}
          userRegularTaxLaw={userRegularTaxLaw}
          userRegularTaxPolicy={userRegularTaxPolicy}
          userAmtLaw={userAmtLaw}
          userAmtPolicy={userAmtPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        Additional SALT does not reduce your income tax if AMT exceeds regular tax.
      </Text>
    </Stack>
  );
}
