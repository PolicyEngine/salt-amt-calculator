/**
 * TDD tests for HouseholdInputs component.
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { HouseholdInputs } from './HouseholdInputs';
import { useStore } from '@/store';

// Mock the store
vi.mock('@/store', () => ({
  useStore: vi.fn(),
}));

const mockSetHousehold = vi.fn();

const renderWithMantine = (component: React.ReactNode) => {
  return render(<MantineProvider>{component}</MantineProvider>);
};

describe('HouseholdInputs', () => {
  beforeEach(() => {
    vi.mocked(useStore).mockReturnValue({
      household: {
        stateCode: 'CA',
        isMarried: false,
        numChildren: 0,
        childAges: [],
        employmentIncome: 100000,
        realEstateTaxes: 10000,
        qualifiedDividendIncome: 0,
        longTermCapitalGains: 0,
        shortTermCapitalGains: 0,
        deductibleMortgageInterest: 0,
        charitableCashDonations: 0,
      },
      setHousehold: mockSetHousehold,
    } as any);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders state selector', () => {
    renderWithMantine(<HouseholdInputs />);
    expect(screen.getByRole('textbox', { name: /^state$/i })).toBeInTheDocument();
  });

  it('renders marriage checkbox', () => {
    renderWithMantine(<HouseholdInputs />);
    expect(screen.getByLabelText(/married/i)).toBeInTheDocument();
  });

  it('renders employment income input', () => {
    renderWithMantine(<HouseholdInputs />);
    expect(screen.getByLabelText(/employment income/i)).toBeInTheDocument();
  });

  it('renders real estate taxes input', () => {
    renderWithMantine(<HouseholdInputs />);
    expect(screen.getByLabelText(/real estate taxes/i)).toBeInTheDocument();
  });

  it('renders number of children input', () => {
    renderWithMantine(<HouseholdInputs />);
    expect(screen.getByLabelText(/children/i)).toBeInTheDocument();
  });

  it('calls setHousehold when marriage checkbox is toggled', () => {
    renderWithMantine(<HouseholdInputs />);
    const checkbox = screen.getByLabelText(/married/i);
    fireEvent.click(checkbox);
    expect(mockSetHousehold).toHaveBeenCalled();
  });
});
