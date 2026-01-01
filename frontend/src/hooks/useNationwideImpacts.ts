/**
 * Hook for loading nationwide impacts data from JSON files.
 */

import { useState, useEffect, useCallback } from 'react';

interface ImpactRecord {
  reform: string;
  baseline: string;
  total_income_change: string;
  percent_better_off: string;
  percent_worse_off: string;
  avg_income_change_p10_20: string;
  avg_income_change_p20_30: string;
  avg_income_change_p30_40: string;
  avg_income_change_p40_50: string;
  avg_income_change_p50_60: string;
  avg_income_change_p60_70: string;
  avg_income_change_p70_80: string;
  avg_income_change_p80_90: string;
  avg_income_change_p90_100: string;
  avg_income_change_p100_110: string;
  year?: number;
}

interface ParsedImpact {
  reform: string;
  baseline: string;
  totalIncomeChange: number;
  percentBetterOff: number;
  percentWorseOff: number;
  decileImpacts: {
    decile: string;
    avgImpact: number;
  }[];
  year?: number;
}

interface NationwideImpactsData {
  singleYearImpacts: ParsedImpact[];
  budgetWindowImpacts: Map<number, ParsedImpact[]>;
  isLoading: boolean;
  error: string | null;
}

const decileLabels = [
  '10-20%',
  '20-30%',
  '30-40%',
  '40-50%',
  '50-60%',
  '60-70%',
  '70-80%',
  '80-90%',
  '90-100%',
  'Top 1%',
];

function parseImpactRecord(record: ImpactRecord): ParsedImpact {
  return {
    reform: record.reform,
    baseline: record.baseline,
    totalIncomeChange: parseFloat(record.total_income_change) || 0,
    percentBetterOff: parseFloat(record.percent_better_off) / 100 || 0,
    percentWorseOff: parseFloat(record.percent_worse_off) / 100 || 0,
    decileImpacts: [
      { decile: decileLabels[0], avgImpact: parseFloat(record.avg_income_change_p10_20) || 0 },
      { decile: decileLabels[1], avgImpact: parseFloat(record.avg_income_change_p20_30) || 0 },
      { decile: decileLabels[2], avgImpact: parseFloat(record.avg_income_change_p30_40) || 0 },
      { decile: decileLabels[3], avgImpact: parseFloat(record.avg_income_change_p40_50) || 0 },
      { decile: decileLabels[4], avgImpact: parseFloat(record.avg_income_change_p50_60) || 0 },
      { decile: decileLabels[5], avgImpact: parseFloat(record.avg_income_change_p60_70) || 0 },
      { decile: decileLabels[6], avgImpact: parseFloat(record.avg_income_change_p70_80) || 0 },
      { decile: decileLabels[7], avgImpact: parseFloat(record.avg_income_change_p80_90) || 0 },
      { decile: decileLabels[8], avgImpact: parseFloat(record.avg_income_change_p90_100) || 0 },
      { decile: decileLabels[9], avgImpact: parseFloat(record.avg_income_change_p100_110) || 0 },
    ],
    year: record.year,
  };
}

export function useNationwideImpacts(): NationwideImpactsData & {
  getReformImpact: (reformName: string, baseline: string) => ParsedImpact | undefined;
  getBudgetWindowImpacts: (reformName: string, baseline: string) => ParsedImpact[];
} {
  const [singleYearImpacts, setSingleYearImpacts] = useState<ParsedImpact[]>([]);
  const [budgetWindowImpacts, setBudgetWindowImpacts] = useState<Map<number, ParsedImpact[]>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        // Load single year impacts
        const singleYearResponse = await fetch('/data/impacts_2026.json');
        if (singleYearResponse.ok) {
          const singleYearData: ImpactRecord[] = await singleYearResponse.json();
          setSingleYearImpacts(singleYearData.map(parseImpactRecord));
        }

        // Load budget window impacts (2026-2035)
        const budgetMap = new Map<number, ParsedImpact[]>();
        for (let year = 2026; year <= 2035; year++) {
          const response = await fetch(`/data/impacts_${year}.json`);
          if (response.ok) {
            const yearData: ImpactRecord[] = await response.json();
            budgetMap.set(year, yearData.map(parseImpactRecord));
          }
        }
        setBudgetWindowImpacts(budgetMap);

        setIsLoading(false);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load impacts data';
        setError(message);
        setIsLoading(false);
      }
    }

    loadData();
  }, []);

  const getReformImpact = useCallback(
    (reformName: string, baseline: string): ParsedImpact | undefined => {
      return singleYearImpacts.find(
        (impact) => impact.reform === reformName && impact.baseline === baseline
      );
    },
    [singleYearImpacts]
  );

  const getBudgetWindowImpacts = useCallback(
    (reformName: string, baseline: string): ParsedImpact[] => {
      const impacts: ParsedImpact[] = [];
      for (let year = 2026; year <= 2035; year++) {
        const yearImpacts = budgetWindowImpacts.get(year);
        if (yearImpacts) {
          const impact = yearImpacts.find(
            (i) => i.reform === reformName && i.baseline === baseline
          );
          if (impact) {
            impacts.push({ ...impact, year });
          }
        }
      }
      return impacts;
    },
    [budgetWindowImpacts]
  );

  return {
    singleYearImpacts,
    budgetWindowImpacts,
    isLoading,
    error,
    getReformImpact,
    getBudgetWindowImpacts,
  };
}
