/**
 * Tests for SaltDeductionChart component.
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { SaltDeductionChart } from './SaltDeductionChart';

// Mock Recharts to avoid rendering issues in tests
vi.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="recharts-container">{children}</div>
  ),
  LineChart: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="recharts-line-chart">{children}</div>
  ),
  Line: () => <div data-testid="recharts-line" />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  Legend: () => <div />,
  ReferenceDot: () => <div />,
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
  it('renders the recharts chart', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
      />
    );
    expect(screen.getByTestId('recharts-container')).toBeInTheDocument();
  });

  it('renders with showCurrentPolicy=false', () => {
    renderWithMantine(
      <SaltDeductionChart
        currentLawData={mockData}
        currentPolicyData={mockCurrentPolicyData}
        userSalt={25000}
        userDeductionLaw={25000}
        userDeductionPolicy={10000}
        showCurrentPolicy={false}
      />
    );
    expect(screen.getByTestId('recharts-container')).toBeInTheDocument();
  });
});
