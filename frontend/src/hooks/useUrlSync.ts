/**
 * Hook for syncing state with URL parameters and postMessage for iframe embedding.
 */

import { useEffect, useCallback } from 'react';
import { useStore } from '@/store';
import type { HouseholdInput, BaselineScenario } from '@/types';

interface UrlParams {
  state?: string;
  income?: string;
  propertyTax?: string;
  married?: string;
  children?: string;
  slide?: string;
  baseline?: string;
}

export function useUrlSync() {
  const {
    household,
    baselineScenario,
    slideIndex,
    setHousehold,
    setBaselineScenario,
    setSlideIndex,
  } = useStore();

  // Parse URL params on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const urlParams: UrlParams = {
      state: params.get('state') || undefined,
      income: params.get('income') || undefined,
      propertyTax: params.get('propertyTax') || undefined,
      married: params.get('married') || undefined,
      children: params.get('children') || undefined,
      slide: params.get('slide') || undefined,
      baseline: params.get('baseline') || undefined,
    };

    // Apply URL params to state
    const updates: Partial<HouseholdInput> = {};
    if (urlParams.state) updates.stateCode = urlParams.state;
    if (urlParams.income) updates.employmentIncome = parseInt(urlParams.income, 10);
    if (urlParams.propertyTax) updates.realEstateTaxes = parseInt(urlParams.propertyTax, 10);
    if (urlParams.married) updates.isMarried = urlParams.married === 'true';
    if (urlParams.children) updates.numChildren = parseInt(urlParams.children, 10);

    if (Object.keys(updates).length > 0) {
      setHousehold(updates);
    }

    if (urlParams.slide) {
      setSlideIndex(parseInt(urlParams.slide, 10));
    }

    if (urlParams.baseline && (urlParams.baseline === 'Current Law' || urlParams.baseline === 'Current Policy')) {
      setBaselineScenario(urlParams.baseline as BaselineScenario);
    }
  }, [setHousehold, setBaselineScenario, setSlideIndex]);

  // Update URL when state changes
  const syncToUrl = useCallback(() => {
    const params = new URLSearchParams();
    params.set('state', household.stateCode);
    params.set('income', household.employmentIncome.toString());
    params.set('propertyTax', household.realEstateTaxes.toString());
    params.set('married', household.isMarried.toString());
    params.set('children', household.numChildren.toString());
    params.set('slide', slideIndex.toString());
    params.set('baseline', baselineScenario);

    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState(null, '', newUrl);

    // Send postMessage to parent (for iframe embedding)
    if (window.parent !== window) {
      window.parent.postMessage(
        {
          type: 'urlUpdate',
          params: params.toString(),
        },
        '*'
      );
    }
  }, [household, slideIndex, baselineScenario]);

  // Sync to URL on state changes (debounced)
  useEffect(() => {
    const timeoutId = setTimeout(syncToUrl, 100);
    return () => clearTimeout(timeoutId);
  }, [syncToUrl]);

  // Listen for postMessage from parent
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'setParams') {
        const params = new URLSearchParams(event.data.params);
        const slide = params.get('slide');
        if (slide) {
          setSlideIndex(parseInt(slide, 10));
        }
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [setSlideIndex]);

  return { syncToUrl };
}
