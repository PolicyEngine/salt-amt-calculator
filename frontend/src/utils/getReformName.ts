/**
 * Construct reform name to match CSV format based on policy config and baseline.
 * Ported from nationwide_impacts/impacts.py get_reform_name().
 */

import type { PolicyConfig, BaselineScenario } from '@/types';

export function getReformName(
  policyConfig: PolicyConfig,
  baseline: BaselineScenario,
  year?: number
): string {
  // SALT component
  let saltFull: string;
  if (policyConfig.saltRepealed || policyConfig.saltCap === 'Repeal SALT') {
    saltFull = 'salt_0_cap';
  } else if (policyConfig.saltCap === 'Current Law (Uncapped)') {
    saltFull = 'salt_uncapped';
  } else if (policyConfig.saltCap === '$15k') {
    if (policyConfig.saltMarriageBonus) {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_15_30_k_with_phaseout'
        : 'salt_15_30_k_without_phaseout';
    } else {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_15_k_with_phaseout'
        : 'salt_15_k_without_phaseout';
    }
  } else if (policyConfig.saltCap === '$100k') {
    if (policyConfig.saltMarriageBonus) {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_100_200k_with_phaseout'
        : 'salt_100_200k_without_phaseout';
    } else {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_100k_with_phaseout'
        : 'salt_100k_without_phaseout';
    }
  } else if (policyConfig.saltCap === 'Current Policy ($10k)') {
    if (policyConfig.saltMarriageBonus) {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_tcja_married_bonus_and_phase_out'
        : 'salt_tcja_base_with_married_bonus';
    } else {
      saltFull = policyConfig.saltPhaseout !== 'None'
        ? 'salt_tcja_base_with_phaseout'
        : 'salt_tcja_base';
    }
  } else {
    saltFull = 'salt_uncapped';
  }

  // AMT component
  let amtSuffix: string;
  if (policyConfig.amtRepealed) {
    amtSuffix = '_amt_repealed';
  } else {
    const exemption = policyConfig.amtExemption;
    const phaseout = policyConfig.amtPhaseout;
    if (exemption === 'Current Law ($70,500 Single, $109,500 Joint)') {
      if (policyConfig.amtEliminateMarriagePenalty) {
        amtSuffix = '_amt_tcja_nmp';
      } else if (phaseout === 'Current Law ($156,700 Single, $209,000 Joint)') {
        amtSuffix = '_amt_tcja_both';
      } else if (phaseout === 'Current Policy ($639,300 Single, $1,278,575 Joint)') {
        amtSuffix = '_amt_pre_tcja_ex_tcja_po';
      } else {
        amtSuffix = '';
      }
    } else if (exemption === 'Current Policy ($89,925 Single, $139,850 Joint)') {
      if (phaseout === 'Current Policy ($639,300 Single, $1,278,575 Joint)') {
        amtSuffix = '_amt_pre_tcja_ex_pre_tcja_po';
      } else if (phaseout === 'Current Law ($156,700 Single, $209,000 Joint)') {
        amtSuffix = '_amt_tcja_ex_pre_tcja_po';
      } else {
        amtSuffix = '';
      }
    } else {
      amtSuffix = '';
    }
  }

  const behavioralSuffix = policyConfig.behavioralResponses
    ? '_behavioral_responses_yes'
    : '_behavioral_responses_no';

  const otherTcjaSuffix = policyConfig.otherTcjaProvisionsExtended === 'Current Law'
    ? '_other_tcja_provisions_extended_no'
    : '_other_tcja_provisions_extended_yes';

  const baselineSuffix = `_vs_${baseline.toLowerCase().replace(/ /g, '_')}`;

  const yearSuffix = year !== undefined && year >= 2027 ? `_year_${year}` : '';

  return `${saltFull}${amtSuffix}${behavioralSuffix}${otherTcjaSuffix}${yearSuffix}${baselineSuffix}`;
}
