/**
 * Sidebar component with Household and Policy tabs.
 */

import { useState } from 'react';
import { Tabs, Button, Box, Text, Loader } from '@mantine/core';
import { IconHome, IconSettings, IconCalculator } from '@tabler/icons-react';
import { useStore } from '@/store';
import { HouseholdInputs } from '@/components/inputs/HouseholdInputs';
import { PolicyConfigInputs } from '@/components/inputs/PolicyConfigInputs';
import { colors, spacing, typography } from '@/designTokens';
import { calculateSinglePoint, calculateSaltAxis, calculateIncomeAxis } from '@/api/client';

export function Sidebar() {
  const [activeTab, setActiveTab] = useState<string | null>('household');
  const {
    household,
    policyConfig,
    baselineScenario,
    isCalculating,
    setCalculating,
    setSinglePointResult,
    setSaltAxisResult,
    setIncomeAxisResult,
    setBaselineSinglePoint,
    setBaselineSaltAxis,
    setBaselineIncomeAxis,
    setHasCalculated,
    setSlideIndex,
    setError,
  } = useStore();

  const handleCalculate = async () => {
    setCalculating(true);
    setError(null);

    try {
      // Calculate baseline (without policy reform)
      const [baselineSingle, baselineSalt, baselineIncome] = await Promise.all([
        calculateSinglePoint(household, baselineScenario),
        calculateSaltAxis(household, baselineScenario),
        calculateIncomeAxis(household, baselineScenario),
      ]);

      setBaselineSinglePoint(baselineSingle);
      setBaselineSaltAxis(baselineSalt);
      setBaselineIncomeAxis(baselineIncome);

      // Calculate with reform if different from baseline
      const hasReform = policyConfig.saltCap !== 'Current Law (Uncapped)' ||
        policyConfig.saltRepealed ||
        policyConfig.amtRepealed ||
        policyConfig.amtExemption !== 'Current Law ($70,500 Single, $109,500 Joint)';

      if (hasReform) {
        const [reformSingle, reformSalt, reformIncome] = await Promise.all([
          calculateSinglePoint(household, baselineScenario, policyConfig),
          calculateSaltAxis(household, baselineScenario, policyConfig),
          calculateIncomeAxis(household, baselineScenario, policyConfig),
        ]);

        setSinglePointResult(reformSingle);
        setSaltAxisResult(reformSalt);
        setIncomeAxisResult(reformIncome);
      } else {
        setSinglePointResult(baselineSingle);
        setSaltAxisResult(baselineSalt);
        setIncomeAxisResult(baselineIncome);
      }

      setHasCalculated(true);
      setSlideIndex(1); // Go to first content slide
    } catch (error) {
      console.error('Calculation error:', error);
      setError(error instanceof Error ? error.message : 'Calculation failed');
    } finally {
      setCalculating(false);
    }
  };

  return (
    <Box
      style={{
        position: 'fixed',
        left: 0,
        top: 0,
        width: spacing.appShell.navbar.width,
        height: '100vh',
        backgroundColor: colors.background.primary,
        borderRight: `1px solid ${colors.border.light}`,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Header */}
      <Box
        style={{
          padding: spacing.md,
          borderBottom: `1px solid ${colors.border.light}`,
        }}
      >
        <Text
          style={{
            fontSize: typography.fontSize.lg,
            fontWeight: typography.fontWeight.semibold,
            color: colors.primary[700],
          }}
        >
          SALTernative
        </Text>
        <Text
          style={{
            fontSize: typography.fontSize.sm,
            color: colors.text.secondary,
          }}
        >
          SALT & AMT Calculator
        </Text>
      </Box>

      {/* Tabs */}
      <Tabs
        value={activeTab}
        onChange={setActiveTab}
        style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}
      >
        <Tabs.List>
          <Tabs.Tab value="household" leftSection={<IconHome size={16} />}>
            Household
          </Tabs.Tab>
          <Tabs.Tab value="policy" leftSection={<IconSettings size={16} />}>
            Policy
          </Tabs.Tab>
        </Tabs.List>

        <Box style={{ flex: 1, overflow: 'auto', padding: spacing.md }}>
          <Tabs.Panel value="household">
            <HouseholdInputs />
          </Tabs.Panel>

          <Tabs.Panel value="policy">
            <PolicyConfigInputs />
          </Tabs.Panel>
        </Box>
      </Tabs>

      {/* Calculate Button */}
      <Box
        style={{
          padding: spacing.md,
          borderTop: `1px solid ${colors.border.light}`,
        }}
      >
        <Button
          fullWidth
          size="lg"
          leftSection={isCalculating ? <Loader size={16} color="white" /> : <IconCalculator size={20} />}
          onClick={handleCalculate}
          disabled={isCalculating}
          style={{
            backgroundColor: colors.primary[500],
          }}
        >
          {isCalculating ? 'Calculating...' : 'Calculate'}
        </Button>
      </Box>
    </Box>
  );
}
