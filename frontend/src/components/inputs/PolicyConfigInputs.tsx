/**
 * Policy configuration input form component.
 */

import { Stack, Select, Checkbox, Text } from '@mantine/core';
import { useStore } from '@/store';
import {
  SALT_CAP_OPTIONS,
  AMT_EXEMPTION_OPTIONS,
  AMT_PHASEOUT_OPTIONS,
  SALT_PHASEOUT_OPTIONS,
  OTHER_TCJA_OPTIONS,
  BaselineScenario,
} from '@/types';
import { colors, spacing, typography } from '@/designTokens';

const BASELINE_OPTIONS: { value: BaselineScenario; label: string }[] = [
  { value: 'Current Law', label: 'Current Law' },
  { value: 'Current Policy', label: 'Current Policy (TCJA Extended)' },
];

export function PolicyConfigInputs() {
  const {
    policyConfig,
    baselineScenario,
    setPolicyConfig,
    setBaselineScenario,
  } = useStore();

  const saltDisabled = policyConfig.saltRepealed;
  const amtDisabled = policyConfig.amtRepealed;

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
        Baseline scenario
      </Text>

      <Select
        label="Baseline"
        data={BASELINE_OPTIONS}
        value={baselineScenario}
        onChange={(value) => value && setBaselineScenario(value as BaselineScenario)}
        searchable
      />

      <Checkbox
        label="Behavioral responses"
        checked={policyConfig.behavioralResponses}
        onChange={(e) => setPolicyConfig({ behavioralResponses: e.currentTarget.checked })}
        description="Include behavioral responses to tax changes"
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
        SALT reform options
      </Text>

      <Checkbox
        label="Repeal SALT deduction"
        checked={policyConfig.saltRepealed}
        onChange={(e) => setPolicyConfig({ saltRepealed: e.currentTarget.checked })}
      />

      <Select
        label="SALT cap"
        data={[...SALT_CAP_OPTIONS].map((opt: string) => ({ value: opt, label: opt }))}
        value={policyConfig.saltCap}
        onChange={(value) => value && setPolicyConfig({ saltCap: value })}
        searchable
        disabled={saltDisabled}
      />

      <Checkbox
        label="SALT marriage bonus"
        checked={policyConfig.saltMarriageBonus}
        onChange={(e) => setPolicyConfig({ saltMarriageBonus: e.currentTarget.checked })}
        disabled={saltDisabled || policyConfig.saltCap === 'Current Law (Uncapped)'}
        description="Double the SALT cap for married filers"
      />

      <Select
        label="SALT phaseout"
        data={[...SALT_PHASEOUT_OPTIONS].map((opt: string) => ({ value: opt, label: opt }))}
        value={policyConfig.saltPhaseout}
        onChange={(value) => value && setPolicyConfig({ saltPhaseout: value })}
        searchable
        disabled={saltDisabled || policyConfig.saltCap === 'Current Law (Uncapped)'}
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
        AMT reform options
      </Text>

      <Checkbox
        label="Repeal AMT"
        checked={policyConfig.amtRepealed}
        onChange={(e) => setPolicyConfig({ amtRepealed: e.currentTarget.checked })}
      />

      <Select
        label="AMT exemption"
        data={[...AMT_EXEMPTION_OPTIONS].map((opt: string) => ({ value: opt, label: opt }))}
        value={policyConfig.amtExemption}
        onChange={(value) => value && setPolicyConfig({ amtExemption: value })}
        searchable
        disabled={amtDisabled}
      />

      <Select
        label="AMT phaseout"
        data={[...AMT_PHASEOUT_OPTIONS].map((opt: string) => ({ value: opt, label: opt }))}
        value={policyConfig.amtPhaseout}
        onChange={(value) => value && setPolicyConfig({ amtPhaseout: value })}
        searchable
        disabled={amtDisabled}
      />

      <Checkbox
        label="Eliminate AMT marriage penalty"
        checked={policyConfig.amtEliminateMarriagePenalty}
        onChange={(e) => setPolicyConfig({ amtEliminateMarriagePenalty: e.currentTarget.checked })}
        disabled={amtDisabled}
        description="Double the AMT exemption and phaseout thresholds for joint filers"
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
        General
      </Text>

      <Select
        label="Other TCJA provisions"
        data={[...OTHER_TCJA_OPTIONS].map((opt: string) => ({ value: opt, label: opt }))}
        value={policyConfig.otherTcjaProvisionsExtended}
        onChange={(value) => value && setPolicyConfig({ otherTcjaProvisionsExtended: value })}
        description="Whether non-SALT/AMT TCJA provisions are extended"
      />
    </Stack>
  );
}
