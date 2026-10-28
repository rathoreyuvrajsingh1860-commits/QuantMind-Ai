"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import MarketChart, { type MarketBar } from "@/components/MarketChart";

type MarketProfile = {
  symbol: string;
  name: string;
  exchange: string | null;
  country: string | null;
  sector: string | null;
  industry: string | null;
  currency: string | null;
};

type PriceBar = MarketBar & {
  source: string;
  retrieved_at: string;
  adjusted_close?: string | number | null;
};

type PriceHistory = {
  symbol: string;
  start: string;
  end: string;
  count: number;
  data: PriceBar[];
};

type InstrumentSearchResult = MarketProfile;

const API_URL = "http://localhost:8000/api/market";

function isoDate(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function dateMonthsAgo(months: number) {
  const date = new Date();
  date.setMonth(date.getMonth() - months);
  return isoDate(date);
}

function formatPrice(
  value: string | number | null | undefined,
  currency: string,
) {
  if (value == null || !Number.isFinite(Number(value))) return "—";

  try {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(Number(value));
  } catch {
    return `${currency} ${Number(value).toLocaleString("en-IN")}`;
  }
}

function formatDate(value: string) {
  if (!value) return "—";

  const date = new Date(`${value.slice(0, 10)}T12:00:00`);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
}

function formatTimestamp(value: string | undefined) {
  if (!value) return "Unavailable";

  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
      });
}

export default function MarketTerminalPage() {
  const [symbolInput, setSymbolInput] = useState("RELIANCE:NSE");
  const [symbol, setSymbol] = useState("RELIANCE:NSE");
  const [start, setStart] = useState(() => dateMonthsAgo(12));
  const [end, setEnd] = useState(() => isoDate(new Date()));
  const [profile, setProfile] = useState<MarketProfile | null>(null);
  const [history, setHistory] = useState<PriceHistory | null>(null);
  const [mode, setMode] = useState<"candles" | "line">("candles");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searchResults, setSearchResults] = useState<InstrumentSearchResult[]>(
    [],
  );
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  async function searchInstruments(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const query = symbolInput.trim();

    if (!query) {
      setSearchError("Enter a company name or ticker to search.");
      setSearchResults([]);
      setHasSearched(false);
      return;
    }

    setSearching(true);
    setSearchError("");
    setHasSearched(true);

    try {
      const response = await fetch(
        `${API_URL}/search?q=${encodeURIComponent(query)}`,
        { cache: "no-store" },
      );
      const payload = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.detail ?? `Instrument search failed (${response.status}).`,
        );
      }

      if (!Array.isArray(payload)) {
        throw new Error(
          "The instrument search returned an unexpected response.",
        );
      }

      setSearchResults(payload as InstrumentSearchResult[]);
    } catch (err) {
      setSearchResults([]);
      setSearchError(
        err instanceof Error ? err.message : "Unable to search instruments.",
      );
    } finally {
      setSearching(false);
    }
  }

  function selectInstrument(instrument: InstrumentSearchResult) {
    setSymbolInput(instrument.symbol);
    setSearchResults([]);
    setSearchError("");
    setHasSearched(false);
    setSymbol(instrument.symbol);
  }

  const loadMarket = useCallback(async () => {
    if (!symbol.trim()) {
      setError("Enter a market symbol.");
      return;
    }

    if (!start || !end || start > end) {
      setError("Choose a valid date range. Start must not be after end.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const encodedSymbol = encodeURIComponent(symbol.trim());
      const query = new URLSearchParams({ start, end });

      const [profileResponse, historyResponse] = await Promise.all([
        fetch(`${API_URL}/${encodedSymbol}/profile`, { cache: "no-store" }),
        fetch(`${API_URL}/${encodedSymbol}/prices?${query.toString()}`, {
          cache: "no-store",
        }),
      ]);

      const profilePayload = await profileResponse.json().catch(() => null);
      const historyPayload = await historyResponse.json().catch(() => null);

      if (!profileResponse.ok) {
        throw new Error(
          profilePayload?.detail ??
            `Profile request failed (${profileResponse.status}).`,
        );
      }

      if (!historyResponse.ok) {
        throw new Error(
          historyPayload?.detail ??
            `Price history request failed (${historyResponse.status}).`,
        );
      }

      setProfile(profilePayload as MarketProfile);
      setHistory(historyPayload as PriceHistory);
      setSymbol(symbol.trim());
    } catch (err) {
      setProfile(null);
      setHistory(null);
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load market data. Check that the API is running.",
      );
    } finally {
      setLoading(false);
    }
  }, [symbol, start, end]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadMarket();
    }, 0);

    return () => window.clearTimeout(timer);
  }, [loadMarket]);

  const chartData = useMemo<MarketBar[]>(
    () =>
      (history?.data ?? []).map((bar) => ({
        date: bar.date,
        open: bar.open,
        high: bar.high,
        low: bar.low,
        close: bar.close,
        volume: bar.volume,
      })),
    [history],
  );

  const latestBar = history?.data.at(-1);
  const currency = profile?.currency || "INR";
  const sources = [...new Set((history?.data ?? []).map((bar) => bar.source))];
  const latestRetrievedAt = history?.data.reduce<string | undefined>(
    (latest, bar) =>
      !latest || bar.retrieved_at > latest ? bar.retrieved_at : latest,
    undefined,
  );

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSymbol(symbolInput.trim());
  }

  function chooseRange(months: number) {
    setStart(dateMonthsAgo(months));
    setEnd(isoDate(new Date()));
  }

  return (
    <main className="min-h-screen bg-[#f7f7f5] text-[#171717]">
      <header className="border-b border-black/[0.07] bg-[#f7f7f5]">
        <div className="mx-auto flex min-h-16 max-w-[1440px] items-center justify-between gap-4 px-5 sm:px-8 lg:px-10">
          <Link href="/" className="flex items-center gap-3">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#171717] text-sm font-semibold text-white">
              Q
            </span>
            <span className="text-sm font-semibold tracking-tight">
              QuantMind AI
            </span>
          </Link>

          <nav className="flex items-center gap-5 text-sm">
            <Link
              href="/"
              className="text-black/50 transition hover:text-black"
            >
              Research
            </Link>
            <span className="font-medium">Market Terminal</span>
          </nav>
        </div>
      </header>

      <div className="mx-auto max-w-[1440px] px-5 py-8 sm:px-8 lg:px-10 lg:py-10">
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-black/40">
              Market workspace
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">
              Market Terminal
            </h1>
            <p className="mt-2 max-w-xl text-sm leading-6 text-black/50">
              Explore historical market prices with candlesticks, volume, and
              closing-price trends.
            </p>
          </div>

          <span className="w-fit rounded-full border border-black/10 bg-white px-3 py-1.5 text-[11px] text-black/55">
            Historical daily data · Not live quotes
          </span>
        </div>

        <form
          onSubmit={handleSubmit}
          className="mt-8 grid gap-4 rounded-2xl border border-black/[0.08] bg-white p-5 sm:grid-cols-2 lg:grid-cols-[minmax(220px,1.4fr)_minmax(150px,1fr)_minmax(150px,1fr)_auto] lg:items-end"
        >
          <div className="block">
            <label className="mb-2 block text-xs font-medium text-black/55">
              Symbol or company
            </label>
            <div className="flex gap-2">
              <input
                value={symbolInput}
                onChange={(event) => setSymbolInput(event.target.value)}
                placeholder="Search Reliance, AAPL…"
                aria-label="Company name or market symbol"
                className="h-11 min-w-0 flex-1 rounded-lg border border-black/10 bg-[#fafaf8] px-3 text-sm outline-none transition focus:border-[#527b68]"
              />
              <button
                type="button"
                onClick={(event) => {
                  const form = event.currentTarget.form;
                  if (form)
                    void searchInstruments({
                      preventDefault: () => {},
                      currentTarget: form,
                    } as FormEvent<HTMLFormElement>);
                }}
                disabled={searching}
                className="h-11 rounded-lg border border-black/10 px-3 text-sm font-medium transition hover:bg-[#fafaf8] disabled:opacity-60"
              >
                {searching ? "Searching…" : "Search"}
              </button>
            </div>
          </div>

          <label className="block">
            <span className="mb-2 block text-xs font-medium text-black/55">
              Start date
            </span>
            <input
              type="date"
              value={start}
              max={end}
              onChange={(event) => setStart(event.target.value)}
              className="h-11 w-full rounded-lg border border-black/10 bg-[#fafaf8] px-3 text-sm outline-none focus:border-[#527b68]"
            />
          </label>

          <label className="block">
            <span className="mb-2 block text-xs font-medium text-black/55">
              End date
            </span>
            <input
              type="date"
              value={end}
              min={start}
              onChange={(event) => setEnd(event.target.value)}
              className="h-11 w-full rounded-lg border border-black/10 bg-[#fafaf8] px-3 text-sm outline-none focus:border-[#527b68]"
            />
          </label>

          <button
            type="submit"
            disabled={loading}
            className="h-11 rounded-lg bg-[#171717] px-5 text-sm font-medium text-white transition hover:bg-black/75 disabled:cursor-wait disabled:opacity-60"
          >
            {loading ? "Loading…" : "Load market"}
          </button>

          <div className="flex flex-wrap items-center gap-2 sm:col-span-2 lg:col-span-4">
            <span className="mr-1 text-xs text-black/40">Quick range</span>
            {[
              { label: "1M", months: 1 },
              { label: "3M", months: 3 },
              { label: "6M", months: 6 },
              { label: "1Y", months: 12 },
            ].map((range) => (
              <button
                key={range.label}
                type="button"
                onClick={() => chooseRange(range.months)}
                className="rounded-md border border-black/10 px-3 py-1.5 text-xs text-black/60 transition hover:border-black/30 hover:bg-[#fafaf8]"
              >
                {range.label}
              </button>
            ))}
          </div>
        </form>

        {(searchError ||
          (hasSearched && searchResults.length === 0 && !searching)) && (
          <div
            role={searchError ? "alert" : "status"}
            className="mt-4 rounded-xl border border-black/[0.08] bg-white px-4 py-3 text-sm text-black/60"
          >
            {searchError ||
              "No instruments found. Try another company name or ticker."}
          </div>
        )}

        {searchResults.length > 0 && (
          <section
            aria-label="Instrument search results"
            className="mt-4 overflow-hidden rounded-xl border border-black/[0.08] bg-white"
          >
            <div className="border-b border-black/[0.07] px-4 py-3">
              <p className="text-xs font-medium text-black/50">
                Search results · Select an instrument to load its chart
              </p>
            </div>
            <ul className="divide-y divide-black/[0.06]">
              {searchResults.map((instrument) => (
                <li key={`${instrument.symbol}-${instrument.exchange ?? ""}`}>
                  <button
                    type="button"
                    onClick={() => selectInstrument(instrument)}
                    className="flex w-full flex-col gap-1 px-4 py-3 text-left transition hover:bg-[#fafaf8] sm:flex-row sm:items-center sm:justify-between"
                  >
                    <span className="min-w-0">
                      <span className="block text-sm font-medium">
                        {instrument.name}
                      </span>
                      <span className="mt-1 block text-xs text-black/45">
                        {instrument.symbol}
                      </span>
                    </span>
                    <span className="text-xs text-black/45 sm:text-right">
                      {[instrument.exchange, instrument.currency]
                        .filter(Boolean)
                        .join(" · ") || "Exchange details unavailable"}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}

        {error && (
          <div
            role="alert"
            className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800"
          >
            <p className="font-medium">Market data could not be loaded</p>
            <p className="mt-1 break-words">{error}</p>
            <p className="mt-2 text-xs text-red-700/80">
              Confirm the FastAPI server is running and that the symbol is
              supported by your configured provider.
            </p>
          </div>
        )}

        <section className="mt-6 rounded-2xl border border-black/[0.08] bg-white p-5 sm:p-7">
          {loading && !history ? (
            <div className="flex min-h-72 items-center justify-center text-sm text-black/40">
              Fetching instrument profile and historical prices…
            </div>
          ) : profile && history ? (
            <>
              <div className="flex flex-col justify-between gap-5 border-b border-black/[0.07] pb-6 sm:flex-row sm:items-start">
                <div>
                  <p className="text-xs text-black/40">
                    {[profile.exchange, profile.country, currency]
                      .filter(Boolean)
                      .join(" · ")}
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold tracking-tight">
                    {profile.name}
                  </h2>
                  <p className="mt-1 font-mono text-xs text-black/40">
                    {profile.symbol}
                  </p>
                  {(profile.sector || profile.industry) && (
                    <p className="mt-3 text-xs text-black/50">
                      {[profile.sector, profile.industry]
                        .filter(Boolean)
                        .join(" · ")}
                    </p>
                  )}
                </div>

                <div className="sm:text-right">
                  <p className="text-[11px] uppercase tracking-[0.14em] text-black/40">
                    Latest available close
                  </p>
                  <p className="mt-2 text-3xl font-semibold tracking-tight">
                    {formatPrice(latestBar?.close, currency)}
                  </p>
                  <p className="mt-1 text-xs text-black/40">
                    {latestBar ? formatDate(latestBar.date) : "No observations"}
                  </p>
                </div>
              </div>

              <div className="mt-6 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                <div>
                  <h3 className="text-sm font-semibold">Price history</h3>
                  <p className="mt-1 text-xs text-black/40">
                    {formatDate(history.start)} – {formatDate(history.end)} ·{" "}
                    {history.count} observations
                  </p>
                </div>

                <div className="flex w-fit rounded-lg border border-black/10 bg-[#fafaf8] p-1">
                  <button
                    type="button"
                    onClick={() => setMode("candles")}
                    aria-pressed={mode === "candles"}
                    className={`rounded-md px-3 py-2 text-xs transition ${
                      mode === "candles"
                        ? "bg-white font-medium text-black shadow-sm"
                        : "text-black/45 hover:text-black"
                    }`}
                  >
                    Candles + volume
                  </button>
                  <button
                    type="button"
                    onClick={() => setMode("line")}
                    aria-pressed={mode === "line"}
                    className={`rounded-md px-3 py-2 text-xs transition ${
                      mode === "line"
                        ? "bg-white font-medium text-black shadow-sm"
                        : "text-black/45 hover:text-black"
                    }`}
                  >
                    Line
                  </button>
                </div>
              </div>

              <div className="mt-4 rounded-xl bg-[#fafaf8] p-2 sm:p-4">
                <MarketChart
                  data={chartData}
                  mode={mode}
                  currency={currency}
                  height={440}
                />
              </div>

              <div className="mt-6 grid gap-4 border-t border-black/[0.07] pt-5 sm:grid-cols-2 lg:grid-cols-4">
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-[0.13em] text-black/40">
                    First open
                  </p>
                  <p className="mt-2 text-sm font-medium">
                    {formatPrice(history.data[0]?.open, currency)}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-[0.13em] text-black/40">
                    Period high
                  </p>
                  <p className="mt-2 text-sm font-medium">
                    {formatPrice(
                      history.data.length
                        ? Math.max(
                            ...history.data.map((bar) => Number(bar.high)),
                          )
                        : null,
                      currency,
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-[0.13em] text-black/40">
                    Period low
                  </p>
                  <p className="mt-2 text-sm font-medium">
                    {formatPrice(
                      history.data.length
                        ? Math.min(
                            ...history.data.map((bar) => Number(bar.low)),
                          )
                        : null,
                      currency,
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-[0.13em] text-black/40">
                    Latest volume
                  </p>
                  <p className="mt-2 text-sm font-medium">
                    {latestBar?.volume == null
                      ? "Unavailable"
                      : Number(latestBar.volume).toLocaleString("en-IN")}
                  </p>
                </div>
              </div>

              <div className="mt-6 rounded-xl border border-black/[0.07] bg-[#fafaf8] p-4">
                <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-black/40">
                  Data provenance
                </p>
                <div className="mt-3 grid gap-3 text-xs text-black/55 sm:grid-cols-3">
                  <p>
                    <span className="block text-black/35">Provider/source</span>
                    <span className="mt-1 block break-words">
                      {sources.length ? sources.join(", ") : "Not reported"}
                    </span>
                  </p>
                  <p>
                    <span className="block text-black/35">Retrieved at</span>
                    <span className="mt-1 block">
                      {formatTimestamp(latestRetrievedAt)}
                    </span>
                  </p>
                  <p>
                    <span className="block text-black/35">Data type</span>
                    <span className="mt-1 block">
                      Historical daily observations
                    </span>
                  </p>
                </div>
                <p className="mt-3 text-[11px] leading-5 text-black/40">
                  The chart displays data returned by the configured market-data
                  provider. The latest available historical close is not
                  necessarily the current market price.
                </p>
              </div>
            </>
          ) : (
            <div className="flex min-h-64 items-center justify-center text-center">
              <div>
                <p className="text-sm font-medium">No market data loaded</p>
                <p className="mt-2 text-xs text-black/45">
                  Enter a supported symbol and choose a date range to begin.
                </p>
              </div>
            </div>
          )}
        </section>

        <footer className="mt-6 flex flex-col justify-between gap-2 text-[11px] text-black/35 sm:flex-row">
          <span>QuantMind AI · Think Beyond the Market.</span>
          <span>Historical data only · Not investment advice</span>
        </footer>
      </div>
    </main>
  );
}
