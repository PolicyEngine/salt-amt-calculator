import { useState } from 'react';
import { MantineProvider, AppShell, Burger, Group, Text, Button, Loader, Tabs, Box, ScrollArea } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconHome, IconSettings, IconCalculator } from '@tabler/icons-react';
import '@mantine/core/styles.css';
import { theme } from './theme';
import { useStore } from './store';
import { SlideNavigation } from './components/layout/SlideNavigation';
import { SlideContainer } from './components/layout/SlideContainer';
import { NotesFooter } from './components/layout/NotesFooter';
import { HouseholdInputs } from './components/inputs/HouseholdInputs';
import { PolicyConfigInputs } from './components/inputs/PolicyConfigInputs';
import { useUrlSync } from './hooks/useUrlSync';
import { calculateSinglePoint, calculateSaltAxis, calculateIncomeAxis } from './api/client';
import { colors, spacing, typography } from './designTokens';

export default function App() {
  const [opened, { toggle }] = useDisclosure(true);
  const [activeTab, setActiveTab] = useState<string | null>('household');

  const {
    slideIndex,
    hasCalculated,
    isCalculating,
    household,
    policyConfig,
    baselineScenario,
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

  useUrlSync();

  const handleCalculate = async () => {
    setCalculating(true);
    setError(null);

    try {
      const [baselineSingle, baselineSalt, baselineIncome] = await Promise.all([
        calculateSinglePoint(household, baselineScenario),
        calculateSaltAxis(household, baselineScenario),
        calculateIncomeAxis(household, baselineScenario),
      ]);

      setBaselineSinglePoint(baselineSingle);
      setBaselineSaltAxis(baselineSalt);
      setBaselineIncomeAxis(baselineIncome);

      const hasReform =
        policyConfig.saltCap !== 'Current Law (Uncapped)' ||
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
      setSlideIndex(1);
    } catch (error) {
      console.error('Calculation error:', error);
      setError(error instanceof Error ? error.message : 'Calculation failed');
    } finally {
      setCalculating(false);
    }
  };

  return (
    <MantineProvider theme={theme}>
      <AppShell
        header={{ height: 60 }}
        navbar={{
          width: 320,
          breakpoint: 'sm',
          collapsed: { mobile: !opened, desktop: !opened },
        }}
        padding="md"
      >
        {/* Header */}
        <AppShell.Header>
          <Group h="100%" px="md" justify="space-between">
            <Group>
              <Burger opened={opened} onClick={toggle} size="sm" />
              <div>
                <Text
                  style={{
                    fontSize: typography.fontSize.lg,
                    fontWeight: typography.fontWeight.bold,
                    color: colors.primary[600],
                    lineHeight: 1.2,
                  }}
                >
                  SALTernative
                </Text>
                <Text size="xs" c="dimmed">SALT & AMT Tax Calculator</Text>
              </div>
            </Group>
            <Button
              size="md"
              leftSection={isCalculating ? <Loader size={16} color="white" /> : <IconCalculator size={18} />}
              onClick={handleCalculate}
              disabled={isCalculating}
              color="primary"
            >
              {isCalculating ? 'Calculating...' : 'Calculate'}
            </Button>
          </Group>
        </AppShell.Header>

        {/* Navbar/Sidebar */}
        <AppShell.Navbar p="md">
          <AppShell.Section>
            <Text
              style={{
                fontSize: typography.fontSize.md,
                fontWeight: typography.fontWeight.semibold,
                color: colors.text.primary,
                marginBottom: spacing.sm,
              }}
            >
              Settings
            </Text>
          </AppShell.Section>

          <AppShell.Section grow component={ScrollArea} scrollbarSize={8}>
            <Tabs value={activeTab} onChange={setActiveTab}>
              <Tabs.List>
                <Tabs.Tab value="household" leftSection={<IconHome size={16} />}>
                  Household
                </Tabs.Tab>
                <Tabs.Tab value="policy" leftSection={<IconSettings size={16} />}>
                  Policy
                </Tabs.Tab>
              </Tabs.List>

              <Box mt="md" pr="md">
                <Tabs.Panel value="household">
                  <HouseholdInputs />
                </Tabs.Panel>
                <Tabs.Panel value="policy">
                  <PolicyConfigInputs />
                </Tabs.Panel>
              </Box>
            </Tabs>
          </AppShell.Section>
        </AppShell.Navbar>

        {/* Main Content */}
        <AppShell.Main
          style={{
            backgroundColor: colors.background.secondary,
            display: 'flex',
            flexDirection: 'column',
            minHeight: 'calc(100vh - 60px)',
          }}
        >
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', width: '100%' }}>
            <SlideContainer
              slideIndex={slideIndex}
              hasCalculated={hasCalculated}
              isCalculating={isCalculating}
            />
          </div>
          <div style={{ width: '100%' }}>
            <SlideNavigation />
          </div>
          <div style={{ width: '100%' }}>
            <NotesFooter />
          </div>
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
}
