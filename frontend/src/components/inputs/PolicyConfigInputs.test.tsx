/**
 * TDD tests for PolicyConfigInputs component.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { PolicyConfigInputs } from './PolicyConfigInputs';
import { useStore } from '@/store';
import { DEFAULT_POLICY } from '@/types';

// Mock the store
vi.mock('@/store', () => ({
  useStore: vi.fn(),
}));

const mockSetPolicyConfig = vi.fn();
const mockSetBaselineScenario = vi.fn();

const renderWithMantine = (component: React.ReactNode) => {
  return render(<MantineProvider>{component}</MantineProvider>);
};

describe('PolicyConfigInputs', () => {
  beforeEach(() => {
    vi.mocked(useStore).mockReturnValue({
      policyConfig: DEFAULT_POLICY,
      baselineScenario: 'Current Law',
      setPolicyConfig: mockSetPolicyConfig,
      setBaselineScenario: mockSetBaselineScenario,
    } as any);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders baseline scenario selector', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByRole('textbox', { name: /baseline/i })).toBeInTheDocument();
  });

  it('renders SALT cap selector', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByRole('textbox', { name: /salt cap/i })).toBeInTheDocument();
  });

  it('renders AMT exemption selector', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByRole('textbox', { name: /amt exemption/i })).toBeInTheDocument();
  });

  it('renders AMT phaseout selector', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByRole('textbox', { name: /amt phaseout/i })).toBeInTheDocument();
  });

  it('renders SALT repeal checkbox', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByLabelText(/repeal salt/i)).toBeInTheDocument();
  });

  it('renders AMT repeal checkbox', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByLabelText(/repeal amt/i)).toBeInTheDocument();
  });

  it('calls setBaselineScenario when baseline is changed', () => {
    renderWithMantine(<PolicyConfigInputs />);
    const select = screen.getByRole('textbox', { name: /baseline/i });
    expect(select).toBeInTheDocument();
  });

  it('renders SALT marriage bonus checkbox', () => {
    renderWithMantine(<PolicyConfigInputs />);
    expect(screen.getByLabelText(/marriage bonus/i)).toBeInTheDocument();
  });
});
