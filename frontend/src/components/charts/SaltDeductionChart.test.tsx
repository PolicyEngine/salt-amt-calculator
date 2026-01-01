/**
 * TDD tests for SaltDeductionChart component.
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { SaltDeductionChart } from './SaltDeductionChart';

// Mock Plotly to avoid rendering issues in tests
vi.mock('react-plotly.js', () => ({
  default: ({ data, layout }: { data: unknown[]; layout: unknown }) => (
    <div data-testid="plotly-chart">
      <div data-testid="plot-data">{JSON.stringify(data)}</div>
      <div data-testid="plot-layout">{JSON.stringify(layout)}</div>
    </div>
  ),
}));

const renderWithMantine = (component: React.ReactNode) => {
  return render(<MantineProvider>{component}</MantineProvider>);
};

const mockData = {
  axisValues: [0, 10000, 20000, 30000, 40000, 50000],
  saltDeduction: [0, 10000, 20000, 30000, 40000, 50000],
};

const mockCurrentPolicyData = {
  axisValues: [0, 10000, 20000, 30000, 40000, 50000],
  saltDeduction: [0, 10000, 10000, 10000, 10000, 10000],
};

describe('SaltDeductionChart', () => {
  it('renders the plotly chart', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
      />
    );
    expect(screen.getByTestId('plotly-chart')).toBeInTheDocument();
  });

  it('includes current law data in the chart', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
      />
    );
    const plotData = screen.getByTestId('plot-data').textContent;
    expect(plotData).toContain('Current Law');
  });

  it('includes current policy data in the chart', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
        showCurrentPolicy={true}
      />
    );
    const plotData = screen.getByTestId('plot-data').textContent;
    expect(plotData).toContain('Current Policy');
  });

  it('includes user household marker', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
      />
    );
    const plotData = screen.getByTestId('plot-data').textContent;
    expect(plotData).toContain('Your household');
  });
});
