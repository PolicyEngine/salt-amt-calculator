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
    expect(screen.getByText('The SALTernative')).toBeInTheDocument();
  });

  it('renders the subtitle or description', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText(/alternative minimum tax/i)).toBeInTheDocument();
  });

  it('renders PolicyEngine branding', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText('PolicyEngine')).toBeInTheDocument();
  });

  it('provides instructions for getting started', () => {
    renderWithMantine(<IntroductionSlide />);
    expect(screen.getByText(/how to use this calculator/i)).toBeInTheDocument();
  });
});
