/**
 * Container that renders the appropriate slide based on index.
 */

import { Box, Text, Loader, Card } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { useStore } from '@/store';
import {
  IntroductionSlide,
  SaltFederalTaxSlide,
  SaltDeductionSlide,
  TaxableIncomeAmtiSlide,
  RegularTaxAmtSlide,
  IncomeTaxSlide,
  TransitionSlide,
  EffectiveSaltCapSlide,
  RegularTaxAmtByIncomeSlide,
  GapSlide,
  MarginalRateSlide,
  TaxSavingsSlide,
  BudgetaryImpactsSlide,
  DistributionalImpactsSlide,
  KeyTakeawaysSlide,
} from '@/components/slides';

interface SlideContainerProps {
  slideIndex: number;
  hasCalculated: boolean;
  isCalculating: boolean;
}

export function SlideContainer({ slideIndex, hasCalculated, isCalculating }: SlideContainerProps) {
  const {
    household,
    singlePointResult,
    saltAxisResult,
    incomeAxisResult,
    baselineSinglePoint,
    baselineSaltAxis,
    baselineIncomeAxis,
    baselineScenario,
  } = useStore();

  // Show loading state
  if (isCalculating) {
    return (
      <Box
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: spacing.md,
          flex: 1,
          width: '100%',
        }}
      >
        <Loader size="xl" color={colors.primary[500]} />
        <Text style={{ color: colors.text.secondary }}>
          Running PolicyEngine simulations...
        </Text>
      </Box>
    );
  }

  // Show introduction on slide 0
  if (slideIndex === 0) {
    return <IntroductionSlide />;
  }

  // Show message if not calculated yet
  if (!hasCalculated) {
    return (
      <Card
        style={{
          maxWidth: '600px',
          textAlign: 'center',
          padding: spacing.xl,
        }}
      >
        <Text
          style={{
            fontSize: typography.fontSize.xl,
            fontWeight: typography.fontWeight.semibold,
            color: colors.text.primary,
            marginBottom: spacing.md,
          }}
        >
          Ready to Calculate
        </Text>
        <Text style={{ color: colors.text.secondary }}>
          Fill out your household information and policy options in the sidebar,
          then click "Calculate" to see your personalized tax analysis.
        </Text>
      </Card>
    );
  }

  // Ensure we have data
  if (!singlePointResult || !saltAxisResult || !baselineSinglePoint || !baselineSaltAxis) {
    return (
      <Card style={{ padding: spacing.xl }}>
        <Text style={{ color: colors.text.secondary }}>Loading data...</Text>
      </Card>
    );
  }

  // Slide rendering based on index
  switch (slideIndex) {
    case 1:
      return (
        <SaltFederalTaxSlide
          currentLawResult={singlePointResult}
          currentPolicyResult={baselineSinglePoint}
          realEstateTaxes={household.realEstateTaxes}
        />
      );

    case 2:
      return (
        <SaltDeductionSlide
          currentLawData={saltAxisResult}
          currentPolicyData={baselineSaltAxis}
          userSalt={singlePointResult.reportedSalt}
          userDeductionLaw={singlePointResult.saltDeduction}
          userDeductionPolicy={baselineSinglePoint.saltDeduction}
        />
      );

    case 3:
      return (
        <TaxableIncomeAmtiSlide
          currentLawData={saltAxisResult}
          currentPolicyData={baselineSaltAxis}
          userSalt={singlePointResult.reportedSalt}
          userTaxableIncomeLaw={singlePointResult.taxableIncome}
          userTaxableIncomePolicy={baselineSinglePoint.taxableIncome}
          userAmtiLaw={singlePointResult.amtIncome}
          userAmtiPolicy={baselineSinglePoint.amtIncome}
        />
      );

    case 4:
      return (
        <RegularTaxAmtSlide
          currentLawData={saltAxisResult}
          currentPolicyData={baselineSaltAxis}
          userSalt={singlePointResult.reportedSalt}
          userRegularTaxLaw={singlePointResult.regularTax}
          userRegularTaxPolicy={baselineSinglePoint.regularTax}
          userAmtLaw={singlePointResult.amt}
          userAmtPolicy={baselineSinglePoint.amt}
          effectiveSaltCapDisplay={`$${singlePointResult.reportedSalt.toLocaleString()}`}
        />
      );

    case 5:
      return (
        <IncomeTaxSlide
          currentLawData={saltAxisResult}
          currentPolicyData={baselineSaltAxis}
          userSalt={singlePointResult.reportedSalt}
          userTaxLaw={singlePointResult.federalIncomeTax}
          userTaxPolicy={baselineSinglePoint.federalIncomeTax}
          effectiveSaltCapLaw={`$${singlePointResult.reportedSalt.toLocaleString()}`}
          effectiveSaltCapPolicy="$10,000"
          taxReductionLaw={Math.max(0, baselineSinglePoint.federalIncomeTax - singlePointResult.federalIncomeTax)}
          taxReductionPolicy={0}
        />
      );

    case 6:
      return (
        <TransitionSlide
          title="How does this vary with wages?"
          subtitle="Next, we'll explore how SALT and AMT interact across income levels."
        />
      );

    case 7:
      // Effective SALT Cap - using income axis data
      if (!incomeAxisResult) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      return (
        <EffectiveSaltCapSlide
          incomeValues={incomeAxisResult.axisValues}
          effectiveSaltCap={incomeAxisResult.saltDeduction}
          userIncome={household.employmentIncome}
          userEffectiveSaltCap={singlePointResult.saltDeduction}
          variant="intro"
        />
      );

    case 8:
      if (!incomeAxisResult || !baselineIncomeAxis) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      return (
        <RegularTaxAmtByIncomeSlide
          currentLawData={incomeAxisResult}
          currentPolicyData={baselineIncomeAxis}
          userIncome={household.employmentIncome}
          userRegularTaxLaw={singlePointResult.regularTax}
          userRegularTaxPolicy={baselineSinglePoint.regularTax}
          userAmtLaw={singlePointResult.amt}
          userAmtPolicy={baselineSinglePoint.amt}
        />
      );

    case 9:
      if (!incomeAxisResult || !baselineIncomeAxis) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      return (
        <GapSlide
          currentLawData={incomeAxisResult}
          currentPolicyData={baselineIncomeAxis}
          userIncome={household.employmentIncome}
          userGapLaw={Math.max(0, singlePointResult.regularTax - singlePointResult.amt)}
          userGapPolicy={Math.max(0, baselineSinglePoint.regularTax - baselineSinglePoint.amt)}
        />
      );

    case 10:
      // Marginal rate - we need to compute this from income axis data
      if (!incomeAxisResult || !baselineIncomeAxis) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      // Compute marginal rates from income tax data
      const computeMarginalRates = (incomeTax: number[], incomes: number[]) => {
        const rates: number[] = [];
        for (let i = 0; i < incomeTax.length; i++) {
          if (i === 0) {
            rates.push(0);
          } else {
            const deltaIncome = incomes[i] - incomes[i - 1];
            const deltaTax = incomeTax[i] - incomeTax[i - 1];
            rates.push(deltaIncome > 0 ? deltaTax / deltaIncome : 0);
          }
        }
        return rates;
      };
      return (
        <MarginalRateSlide
          currentLawIncome={incomeAxisResult.axisValues}
          currentLawMarginalRate={computeMarginalRates(incomeAxisResult.incomeTax, incomeAxisResult.axisValues)}
          currentPolicyIncome={baselineIncomeAxis.axisValues}
          currentPolicyMarginalRate={computeMarginalRates(baselineIncomeAxis.incomeTax, baselineIncomeAxis.axisValues)}
          userIncome={household.employmentIncome}
          userMarginalRateLaw={0.32} // Approximate - would need API endpoint
          userMarginalRatePolicy={0.32}
        />
      );

    case 11:
      if (!incomeAxisResult) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      return (
        <EffectiveSaltCapSlide
          incomeValues={incomeAxisResult.axisValues}
          effectiveSaltCap={incomeAxisResult.saltDeduction}
          userIncome={household.employmentIncome}
          userEffectiveSaltCap={singlePointResult.saltDeduction}
          variant="formula"
        />
      );

    case 12:
      if (!incomeAxisResult) {
        return <Card style={{ padding: spacing.xl }}><Text>Loading income data...</Text></Card>;
      }
      // Compute tax savings from income axis data
      const taxSavings = incomeAxisResult.incomeTax.map((tax) => {
        const baseTax = incomeAxisResult.incomeTax[0] || 0;
        return Math.max(0, baseTax - tax);
      });
      return (
        <TaxSavingsSlide
          incomeValues={incomeAxisResult.axisValues}
          taxSavings={taxSavings}
          userIncome={household.employmentIncome}
          userTaxSavings={Math.max(0, baselineSinglePoint.federalIncomeTax - singlePointResult.federalIncomeTax)}
        />
      );

    case 13:
      return (
        <TransitionSlide
          title="How would you reform the SALT deduction and AMT?"
          subtitle="Use the Policy tab in the sidebar to customize your reform, then see the nationwide impacts."
        />
      );

    case 14:
      // Budgetary impacts - placeholder for now
      return (
        <BudgetaryImpactsSlide
          budgetWindowImpacts={[
            { year: 2026, totalIncomeChange: 0 },
            { year: 2027, totalIncomeChange: 0 },
            { year: 2028, totalIncomeChange: 0 },
            { year: 2029, totalIncomeChange: 0 },
            { year: 2030, totalIncomeChange: 0 },
            { year: 2031, totalIncomeChange: 0 },
            { year: 2032, totalIncomeChange: 0 },
            { year: 2033, totalIncomeChange: 0 },
            { year: 2034, totalIncomeChange: 0 },
            { year: 2035, totalIncomeChange: 0 },
          ]}
          totalDeficitChange={0}
          baselineScenario={baselineScenario}
        />
      );

    case 15:
      // Distributional impacts - placeholder for now
      return (
        <DistributionalImpactsSlide
          distributionData={[
            { decile: '10-20%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '20-30%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '30-40%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '40-50%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '50-60%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '60-70%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '70-80%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '80-90%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: '90-100%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
            { decile: 'Top 1%', avgImpact: 0, pctBetterOff: 0, pctWorseOff: 0 },
          ]}
          pctBetterOff={0}
          pctWorseOff={0}
          avgImpactForAffected={0}
          baselineScenario={baselineScenario}
        />
      );

    case 16:
      return <KeyTakeawaysSlide />;

    default:
      return (
        <Card style={{ padding: spacing.xl }}>
          <Text style={{ color: colors.text.secondary }}>
            Slide {slideIndex + 1} placeholder
          </Text>
        </Card>
      );
  }
}
