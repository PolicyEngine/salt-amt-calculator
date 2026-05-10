import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import AppClient from './AppClient';

vi.mock('@policyengine/ui-kit/layout', () => ({
  PolicyEngineHeader: () => (
    <div aria-label="PolicyEngine site header">
      <span>PolicyEngine</span>
      <nav>Research Model API Donate</nav>
    </div>
  ),
}));

vi.mock('@/hooks/useUrlSync', () => ({
  useUrlSync: vi.fn(),
}));

vi.mock('@/components/layout/SlideContainer', () => ({
  SlideContainer: () => <main>Slide content</main>,
}));

vi.mock('@/components/layout/SlideNavigation', () => ({
  SlideNavigation: () => <nav>Slide navigation</nav>,
}));

vi.mock('@/components/layout/NotesFooter', () => ({
  NotesFooter: () => <footer>Notes</footer>,
}));

vi.mock('@/components/inputs/HouseholdInputs', () => ({
  HouseholdInputs: () => <section>Household inputs</section>,
}));

vi.mock('@/components/inputs/PolicyConfigInputs', () => ({
  PolicyConfigInputs: () => <section>Policy inputs</section>,
}));

describe('AppClient shell', () => {
  it('renders the shared PolicyEngine shell before the SALT toolbar', () => {
    render(<AppClient />);

    const appHeader = document.querySelector('header');
    const policyEngineHeader = screen.getAllByLabelText('PolicyEngine site header')[0];
    const saltTitle = screen.getByText('SALTernative');

    expect(appHeader).toContainElement(policyEngineHeader);
    expect(appHeader).toContainElement(saltTitle);
    expect(policyEngineHeader.compareDocumentPosition(saltTitle)).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING,
    );
    expect(appHeader?.firstElementChild).toBe(policyEngineHeader);
  });
});
