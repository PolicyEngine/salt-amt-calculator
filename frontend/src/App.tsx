import { useState } from 'react';
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import { theme } from './theme';
import { useStore } from './store';
import { Header } from './components/layout/Header';
import { InputDrawer } from './components/layout/InputDrawer';
import { SlideNavigation } from './components/layout/SlideNavigation';
import { SlideContainer } from './components/layout/SlideContainer';
import { useUrlSync } from './hooks/useUrlSync';
import { calculateSinglePoint, calculateSaltAxis, calculateIncomeAxis } from './api/client';
import { colors, spacing } from './designTokens';

export default function App() {
  const [drawerOpened, setDrawerOpened] = useState(true); // Start open
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

  // Sync state with URL for iframe embedding
  useUrlSync();

  const handleCalculate = async () => {
    setDrawerOpened(false);
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
      setSlideIndex(1); // Go to first content slide
    } catch (error) {
      console.error('Calculation error:', error);
      setError(error instanceof Error ? error.message : 'Calculation failed');
    } finally {
      setCalculating(false);
    }
  };

  return (
    <MantineProvider theme={theme}>
      {/* Header */}
      <Header
        onMenuClick={() => setDrawerOpened((o) => !o)}
        menuOpened={drawerOpened}
        onCalculate={handleCalculate}
        isCalculating={isCalculating}
      />

      {/* Input Drawer */}
      <InputDrawer opened={drawerOpened} onClose={() => setDrawerOpened(false)} />

      {/* Main Content - Full Width */}
      <main
        style={{
          marginTop: '64px',
          minHeight: 'calc(100vh - 64px)',
          backgroundColor: colors.background.secondary,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Slide Content - Full Width */}
        <div
          style={{
            flex: 1,
            width: '100%',
            padding: spacing.lg,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <SlideContainer
            slideIndex={slideIndex}
            hasCalculated={hasCalculated}
            isCalculating={isCalculating}
          />
        </div>

        {/* Navigation */}
        <SlideNavigation />
      </main>
    </MantineProvider>
  );
}
