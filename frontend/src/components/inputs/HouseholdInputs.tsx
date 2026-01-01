/**
 * Household input form component.
 */

import { Stack, Select, Checkbox, NumberInput, Text } from '@mantine/core';
import { useStore } from '@/store';
import { STATE_CODES } from '@/types';
import { colors, spacing, typography } from '@/designTokens';

export function HouseholdInputs() {
  const { household, setHousehold } = useStore();

  const stateOptions = STATE_CODES.map((code) => ({
    value: code,
    label: code,
  }));

  return (
    <Stack gap={spacing.md}>
      <Text
        style={{
          fontSize: typography.fontSize.sm,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.secondary,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}
      >
        Location & Filing Status
      </Text>

      <Select
        label="State"
        data={stateOptions}
        value={household.stateCode}
        onChange={(value) => value && setHousehold({ stateCode: value })}
        searchable
      />

      <Checkbox
        label="Married filing jointly"
        checked={household.isMarried}
        onChange={(e) => setHousehold({ isMarried: e.currentTarget.checked })}
      />

      <NumberInput
        label="Number of children"
        value={household.numChildren}
        onChange={(value) => setHousehold({ numChildren: Number(value) || 0 })}
        min={0}
        max={10}
      />

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.secondary,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          marginTop: spacing.md,
        }}
      >
        Income
      </Text>

      <NumberInput
        label="Employment income"
        value={household.employmentIncome}
        onChange={(value) => setHousehold({ employmentIncome: Number(value) || 0 })}
        min={0}
        step={1000}
        prefix="$"
        thousandSeparator=","
      />

      <NumberInput
        label="Qualified dividends"
        value={household.qualifiedDividendIncome}
        onChange={(value) =>
          setHousehold({ qualifiedDividendIncome: Number(value) || 0 })
        }
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />

      <NumberInput
        label="Long-term capital gains"
        value={household.longTermCapitalGains}
        onChange={(value) =>
          setHousehold({ longTermCapitalGains: Number(value) || 0 })
        }
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />

      <NumberInput
        label="Short-term capital gains"
        value={household.shortTermCapitalGains}
        onChange={(value) =>
          setHousehold({ shortTermCapitalGains: Number(value) || 0 })
        }
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.secondary,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          marginTop: spacing.md,
        }}
      >
        Deductions
      </Text>

      <NumberInput
        label="Real estate taxes"
        value={household.realEstateTaxes}
        onChange={(value) => setHousehold({ realEstateTaxes: Number(value) || 0 })}
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />

      <NumberInput
        label="Deductible mortgage interest"
        value={household.deductibleMortgageInterest}
        onChange={(value) =>
          setHousehold({ deductibleMortgageInterest: Number(value) || 0 })
        }
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />

      <NumberInput
        label="Charitable donations"
        value={household.charitableCashDonations}
        onChange={(value) =>
          setHousehold({ charitableCashDonations: Number(value) || 0 })
        }
        min={0}
        step={100}
        prefix="$"
        thousandSeparator=","
      />
    </Stack>
  );
}
