/**
 * TDD tests for IntroductionSlide component.
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { IntroductionSlide } from './IntroductionSlide';

const renderWithMantine = (component: React.ReactNode) => {
  return render(<MantineProvider>{component}</MantineProvider>);
};

describe('IntroductionSlide', () => {
  it('renders the title', () => {
    renderWithMantine(<IntroductionSlide />);
    // "SALT" is in a colored span, so match the parent element directly
    expect(screen.getByText(/What/)).toBeInTheDocument();
    expect(screen.getByText('SALT')).toBeInTheDocument();
  });

  it('renders the description about SALT and AMT', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText(/alternative minimum tax/i)).toBeInTheDocument();
  });

  it('renders PolicyEngine branding', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText('PolicyEngine')).toBeInTheDocument();
  });

  it('describes TCJA expiration context', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText(/Tax Cuts and Jobs Act/i)).toBeInTheDocument();
  });
});
