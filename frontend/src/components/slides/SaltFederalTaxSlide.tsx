/**
 * SALT and Federal Income Tax slide - shows SALT breakdown and federal tax comparison.
 */

import { Box, Text, Card, Stack, Table } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import type { SinglePointResult } from '@/types';

interface SaltFederalTaxSlideProps {
  currentLawResult: SinglePointResult;
  currentPolicyResult: SinglePointResult;
  realEstateTaxes: number;
}

export function SaltFederalTaxSlide({
  currentLawResult,
  currentPolicyResult,
  realEstateTaxes,
}: SaltFederalTaxSlideProps) {
  const stateOrSalesTax = currentLawResult.largerOfStateSalesOrIncomeTax;
  const totalSalt = stateOrSalesTax + realEstateTaxes;
  const taxType = currentLawResult.stateIncomeTaxOverSalesTax
    ? 'State Income Tax'
    : 'State Sales Tax';

  const formatCurrency = (value: number) => `$${value.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

  return (
    <Stack gap={spacing.lg}>
      <Card
        style={{
          padding: spacing.lg,
          background: colors.background.secondary,
        }}
      >
        <Text
          style={{
            fontSize: typography.fontSize.lg,
            fontWeight: typography.fontWeight.semibold,
            marginBottom: spacing.md,
          }}
        >
          In 2026, you will pay an estimated{' '}
          <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.bold }}>
            {formatCurrency(stateOrSalesTax)}
          </Text>{' '}
          in {taxType}. Combined with your{' '}
          <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.bold }}>
            {formatCurrency(realEstateTaxes)}
          </Text>{' '}
          in property taxes, this totals{' '}
          <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.bold }}>
            {formatCurrency(totalSalt)}
          </Text>{' '}
          in total SALT.
        </Text>

        <Text
          style={{
            fontSize: typography.fontSize.sm,
            color: colors.text.secondary,
            marginTop: spacing.sm,
          }}
        >
          Federal law allows deducting property taxes and either state and local income taxes,
          or (actual or estimated) state and local sales taxes.
        </Text>
      </Card>

      <Card
        style={{
          padding: spacing.lg,
          background: colors.background.secondary,
        }}
      >
        <Text
          style={{
            fontSize: typography.fontSize.lg,
            fontWeight: typography.fontWeight.semibold,
            marginBottom: spacing.md,
          }}
        >
          You will owe{' '}
          <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.bold }}>
            {formatCurrency(currentLawResult.federalIncomeTax)}
          </Text>{' '}
          in federal income taxes under current law and{' '}
          <Text component="span" style={{ color: colors.primary[500], fontWeight: typography.fontWeight.bold }}>
            {formatCurrency(currentPolicyResult.federalIncomeTax)}
          </Text>{' '}
          under current policy.
        </Text>
      </Card>

      <Box>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Metric</Table.Th>
              <Table.Th>Value</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            <Table.Tr>
              <Table.Td>{taxType}</Table.Td>
              <Table.Td>{formatCurrency(stateOrSalesTax)}</Table.Td>
            </Table.Tr>
            <Table.Tr>
              <Table.Td>Property Taxes</Table.Td>
              <Table.Td>{formatCurrency(realEstateTaxes)}</Table.Td>
            </Table.Tr>
            <Table.Tr>
              <Table.Td style={{ fontWeight: typography.fontWeight.bold }}>Total SALT</Table.Td>
              <Table.Td style={{ fontWeight: typography.fontWeight.bold }}>{formatCurrency(totalSalt)}</Table.Td>
            </Table.Tr>
          </Table.Tbody>
        </Table>
      </Box>
    </Stack>
  );
}
