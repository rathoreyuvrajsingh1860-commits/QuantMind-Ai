"use client";


import { FormEvent, useEffect, useMemo, useState } from "react";


type Evidence = {

  source: string;

  retrieved_at: string | null;

  description: string;

};


type ResearchHistoryItem = {
  id: string;
  query: string;
  status: string;
  model: string | null;
  started_at: string;
  completed_at: string | null;
};

type ResearchResponse = {

  research_run_id: string;

  verification: {

    passed: boolean;

    issues: {

      field: string;

      message: string;

    }[];

  };

  research: {

    query: string;

    entity: {

      symbol: string;

      name: string;

      exchange: string | null;

      country: string | null;

      sector: string | null;

      industry: string | null;

      currency: string | null;

    };

    market: {

      start: string;

      end: string;

      observations: number;

      latest_close: string | null;

      first_close: string | null;

      absolute_change: string | null;

      percentage_change: string | null;

      period_high: string | null;

      period_low: string | null;

      average_close: string | null;

      total_volume: number | null;

    };

    coverage: {

      requested_start: string;

      requested_end: string;

      evidence_start: string | null;

      evidence_end: string | null;

      observations: number;

    };

    evidence: Evidence[];

    limitations: string[];

  };

  ai_analysis: {

    analysis: {

      executive_summary: string;

      key_findings: string[];

      factual_observations: string[];

      interpretation: string[];

      risks: string[];

      uncertainty: string[];

      limitations: string[];

    };

    provider: string;

    model: string;

  } | null;

};


const API_URL = "http\://localhost:8000/api/research";


function formatNumber(value: string | number | null) {

  if (value === null) return "—";


  const number = Number(value);


  return new Intl.NumberFormat("en-IN", {

    maximumFractionDigits: 2,

  }).format(number);

}


function formatPercent(value: string | null) {

  if (value === null) return "—";

  return `${Number(value).toFixed(2)}%`;

}


function formatDate(value: string | null) {

  if (!value) return "—";


  return new Date(value).toLocaleDateString("en-IN", {

    day: "2-digit",

    month: "short",

    year: "numeric",

  });

}


export default function Home() {

  const [query, setQuery] = useState("RELIANCE:BSE");

  const [result, setResult] = useState<ResearchResponse | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [history, setHistory] = useState<ResearchHistoryItem[]>([]);

  const [historyLoading, setHistoryLoading] = useState(true);


  async function loadHistory() {
    try {
      const response = await fetch(`${API_URL}/history?limit=8`);

      if (!response.ok) {
        throw new Error(`History request failed (${response.status})`);
      }

      const data: ResearchHistoryItem[] = await response.json();
      setHistory(data);
    } catch {
      setHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    void loadHistory();
  }, []);

  async function loadResearchRun(id: string) {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/${id}`);

      if (!response.ok) {
        throw new Error(`Unable to load research run (${response.status})`);
      }

      const data: ResearchResponse = await response.json();
      setResult(data);

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load the saved research run.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function runResearch(event?: FormEvent) {

    event?.preventDefault();


    const trimmed = query.trim();


    if (!trimmed) return;


    setLoading(true);

    setError("");


    try {

      const response = await fetch(API_URL, {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

        },

        body: JSON.stringify({

          query: trimmed,

        }),

      });


      if (!response.ok) {

        throw new Error(`Research request failed (${response.status})`);

      }


      const data: ResearchResponse = await response.json();

      setResult(data);
      await loadHistory();

    } catch (err) {

      setError(

        err instanceof Error

          ? err.message

          : "Unable to complete the research request.",

      );

    } finally {

      setLoading(false);

    }

  }


  const market = result?.research.market;

  const entity = result?.research.entity;

  const ai = result?.ai_analysis?.analysis;


  const range = useMemo(() => {

    if (!market?.period_high || !market?.period_low) return null;


    const high = Number(market.period_high);

    const low = Number(market.period_low);

    const latest = Number(market.latest_close);


    if (high === low) return null;


    return {

      high,

      low,

      latest,

      position: Math.max(

        0,

        Math.min(100, ((latest - low) / (high - low)) * 100),

      ),

    };

  }, [market]);


  return (

    <main className="min-h-screen bg-[#f7f7f5] text-[#171717]">

      <header className="border-b border-black/[0.07] bg-[#f7f7f5]/95 backdrop-blur">

        <div className="mx-auto flex h-16 max-w-[1440px] items-center justify-between px-6 lg:px-10">

          <div className="flex items-center gap-3">

            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#171717] text-sm font-semibold text-white">

              Q

            </div>

            <span className="text-[15px] font-semibold tracking-[-0.02em]">

              QuantMind

            </span>

          </div>


          <div className="hidden text-xs text-black/45 sm:block">

            Financial Intelligence

          </div>


          <div className="flex items-center gap-2 text-xs text-black/45">

            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />

            Research system online

          </div>

        </div>

      </header>


      <div className="mx-auto max-w-[1440px] px-6 py-10 lg:px-10 lg:py-14">

        <section className="mx-auto max-w-4xl">

          <div className="mb-5 text-center">

            <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-black/40">

              Research Workspace

            </p>


            <h1 className="text-4xl font-semibold tracking-[-0.045em] sm:text-5xl">

              Intelligence for every

              <br />

              financial decision.

            </h1>


            <p className="mx-auto mt-5 max-w-2xl text-sm leading-6 text-black/50 sm:text-base">

              Research companies using market data, evidence, and explainable

              AI analysis in one workspace.

            </p>

          </div>


          <form onSubmit={runResearch} className="mt-8">

            <div className="flex items-center rounded-2xl border border-black/10 bg-white p-2 shadow-[0_12px_40px_rgba(0,0,0,0.06)]">

              <div className="flex h-11 w-11 shrink-0 items-center justify-center text-black/35">

                ⌕

              </div>


              <input

                value={query}

                onChange={(event) => setQuery(event.target.value)}

                placeholder="Search a company or symbol..."

                className="min-w-0 flex-1 bg-transparent px-1 text-sm outline-none placeholder:text-black/30"

              />


              <button

                type="submit"

                disabled={loading}

                className="rounded-xl bg-[#171717] px-5 py-3 text-xs font-medium text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-50"

              >

                {loading ? "Researching..." : "Research"}

              </button>

            </div>

          </form>


          <div className="mt-3 flex justify-center gap-2 text-[11px] text-black/35">

            <span>Try</span>

            <button

              onClick={() => setQuery("RELIANCE:BSE")}

              className="hover:text-black"

            >

              RELIANCE:BSE

            </button>

            <span>·</span>

            <button

              onClick={() => setQuery("AAPL")}

              className="hover:text-black"

            >

              AAPL

            </button>

          </div>


          <section className="mt-8">
            <div className="rounded-2xl border border-black/[0.08] bg-white p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-black/35">
                    Recent research
                  </p>
                  <p className="mt-1 text-xs text-black/40">
                    Previously completed research runs.
                  </p>
                </div>

                <span className="text-[10px] text-black/30">
                  {history.length} runs
                </span>
              </div>

              <div className="mt-4 divide-y divide-black/[0.06]">
                {historyLoading ? (
                  <div className="py-4 text-xs text-black/35">
                    Loading research history...
                  </div>
                ) : history.length ? (
                  history.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => void loadResearchRun(item.id)}
                      disabled={loading}
                      className="flex w-full flex-col gap-2 py-3 text-left transition hover:bg-black/[0.02] sm:flex-row sm:items-center sm:justify-between disabled:cursor-wait disabled:opacity-60"
                    >
                      <div className="min-w-0">
                        <p className="truncate font-mono text-xs font-medium text-black/70">
                          {item.query}
                        </p>
                        <p className="mt-1 text-[10px] text-black/35">
                          {formatDate(item.completed_at ?? item.started_at)}
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-medium text-emerald-700">
                          {item.status}
                        </span>

                        {item.model && (
                          <span className="max-w-[240px] truncate rounded-full bg-black/[0.04] px-2.5 py-1 text-[10px] text-black/40">
                            {item.model}
                          </span>
                        )}
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="py-4 text-xs text-black/35">
                    No previous research runs yet.
                  </div>
                )}
              </div>
            </div>
          </section>

          {error && (

            <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">

              {error}

            </div>

          )}

        </section>


        {result && entity && market && (

          <section className="mt-14">

            <div className="mb-8 flex flex-col justify-between gap-5 border-b border-black/[0.08] pb-7 sm:flex-row sm:items-end">

              <div>

                <div className="mb-2 flex items-center gap-2 text-xs text-black/40">

                  <span>{entity.exchange}</span>

                  <span>·</span>

                  <span>{entity.country}</span>

                  <span>·</span>

                  <span>{entity.currency}</span>

                </div>


                <h2 className="text-3xl font-semibold tracking-[-0.04em]">

                  {entity.name}

                </h2>


                <p className="mt-1 font-mono text-xs text-black/40">

                  {entity.symbol}

                </p>

              </div>


              <div className="text-left sm:text-right">

                <p className="text-[10px] font-semibold uppercase tracking-[0.15em] text-black/35">

                  Research run

                </p>

                <p className="mt-1 font-mono text-[10px] text-black/45">

                  {result.research_run_id}

                </p>

                <div

                  className={`mt-3 inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-[10px] font-medium ${

                  result.verification.passed

                    ? "border-emerald-200 bg-emerald-50 text-emerald-700"

                    : "border-red-200 bg-red-50 text-red-700"

                }`}

                >

                  <span

                    className={`h-1.5 w-1.5 rounded-full ${

                    result.verification.passed

                      ? "bg-emerald-500"

                      : "bg-red-500"

                  }`}

                />


                {result.verification.passed

                    ? "Verified research"

                    : "Verification failed"}

                </div>

            </div>

          </div>


            <div className="grid gap-5 lg:grid-cols-[1.7fr_1fr]">

              <div className="rounded-2xl border border-black/[0.08] bg-white p-6">

                <div className="flex items-start justify-between gap-5">

                  <div>

                    <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-black/35">

                      Market overview

                    </p>


                    <div className="mt-3 flex items-end gap-3">

                      <span className="text-4xl font-semibold tracking-[-0.04em]">

                        ₹{formatNumber(market.latest_close)}

                      </span>


                      <span

                        className={`mb-1 text-sm font-medium ${

                          Number(market.percentage_change) < 0

                            ? "text-red-600"

                            : "text-emerald-600"

                        }`}

                      >

                        {formatPercent(market.percentage_change)}

                      </span>

                    </div>

                  </div>


                  <div className="text-right text-[11px] text-black/35">

                    <div>{formatDate(market.start)}</div>

                    <div>to {formatDate(market.end)}</div>

                  </div>

                </div>


                <div className="mt-8">

                  <div className="relative h-40 overflow-hidden rounded-xl bg-[#fafaf8]">

                    <div className="absolute inset-x-0 top-1/2 border-t border-dashed border-black/[0.08]" />

                    <div className="absolute inset-x-0 bottom-6 border-t border-black/[0.05]" />


                    <div className="absolute bottom-5 left-5 right-5 h-px bg-black/10">

                      <div

                        className="absolute -top-1.5 h-3 w-3 rounded-full border-2 border-white bg-[#171717] shadow-sm"

                        style={{

                          left: `${range?.position ?? 50}%`,

                        }}

                      />

                    </div>


                    <div className="absolute left-5 top-5 text-[10px] text-black/35">

                      High ₹{formatNumber(market.period_high)}

                    </div>


                    <div className="absolute bottom-10 left-5 text-[10px] text-black/35">

                      Low ₹{formatNumber(market.period_low)}

                    </div>


                    <div className="absolute bottom-10 right-5 text-right text-[10px] text-black/35">

                      <div>Latest</div>

                      <div className="mt-0.5 font-medium text-black/60">

                        ₹{formatNumber(market.latest_close)}

                      </div>

                    </div>

                  </div>


                  <p className="mt-3 text-[10px] text-black/30">

                    Price range indicator · {market.observations} observations

                  </p>

                </div>


                <div className="mt-7 grid grid-cols-2 gap-x-6 gap-y-5 border-t border-black/[0.07] pt-6 sm:grid-cols-4">

                  <Metric

                    label="Period change"

                    value={`₹${formatNumber(market.absolute_change)}`}

                  />

                  <Metric

                    label="Period high"

                    value={`₹${formatNumber(market.period_high)}`}

                  />

                  <Metric

                    label="Period low"

                    value={`₹${formatNumber(market.period_low)}`}

                  />

                  <Metric

                    label="Average close"

                    value={`₹${formatNumber(market.average_close)}`}

                  />

                </div>

              </div>


              <div className="rounded-2xl border border-black/[0.08] bg-white p-6">

                <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-black/35">

                  Data coverage

                </p>


                <div className="mt-6 space-y-5">

                  <Coverage

                    label="Observations"

                    value={formatNumber(market.observations)}

                  />

                  <Coverage

                    label="Total volume"

                    value={formatNumber(market.total_volume)}

                  />

                  <Coverage

                    label="Currency"

                    value={entity.currency ?? "—"}

                  />

                  <Coverage

                    label="Primary source"

                    value={result.research.evidence[0]?.source ?? "—"}

                  />

                </div>


                <div className="mt-7 border-t border-black/[0.07] pt-5">

                  <p className="text-[10px] uppercase tracking-[0.14em] text-black/30">

                    Data principle

                  </p>

                  <p className="mt-2 text-xs leading-5 text-black/50">

                    Deterministic market calculations are kept separate from

                    AI interpretation.

                  </p>

                </div>

              </div>

            </div>


            <div className="mt-5 grid gap-5 lg:grid-cols-[1.4fr_1fr]">

              <div className="rounded-2xl border border-black/[0.08] bg-white p-6">

                <div className="flex items-center justify-between">

                  <div>

                    <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-black/35">

                      AI intelligence

                    </p>

                    <h3 className="mt-2 text-xl font-semibold tracking-[-0.025em]">

                      Research analysis

                    </h3>

                  </div>


                  {result.ai_analysis && (

                    <span className="rounded-full bg-black/[0.04] px-3 py-1 text-[10px] text-black/45">

                      {result.ai_analysis.provider}

                    </span>

                  )}

                </div>


                {ai ? (

                  <div className="mt-7 space-y-7">

                    <div>

                      <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-black/30">

                        Executive summary

                      </p>

                      <p className="mt-2 text-sm leading-6 text-black/70">

                        {ai.executive_summary}

                      </p>

                    </div>


                    <AnalysisList

                      title="Key findings"

                      items={ai.key_findings}

                    />


                    <AnalysisList

                      title="Factual observations"

                      items={ai.factual_observations}

                    />


                    <AnalysisList

                      title="Interpretation"

                      items={ai.interpretation}

                    />


                    <AnalysisList title="Risks" items={ai.risks} />

                  </div>

                ) : (

                  <div className="mt-7 rounded-xl bg-[#fafaf8] p-5">

                    <p className="text-sm font-medium">

                      AI analysis is not configured.

                    </p>

                    <p className="mt-2 text-xs leading-5 text-black/45">

                      The deterministic research pipeline is working. Configure

                      the AI provider to add explainable analysis to this

                      workspace.

                    </p>

                  </div>

                )}

              </div>


              <div className="space-y-5">

                <div className="rounded-2xl border border-black/[0.08] bg-white p-6">

                  <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-black/35">

                    Evidence

                  </p>


                  <p className="mt-2 text-xs leading-5 text-black/45">

                    Source-backed market observations used in this research run.

                  </p>

                  <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">

                    <div className="rounded-xl border border-black/[0.06] bg-black/[0.015] p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-black/35">
                        Requested period
                      </p>

                      <p className="mt-1 text-xs font-medium text-black/70">
                        {formatDate(result.research.coverage.requested_start)}
                        {" → "}
                        {formatDate(result.research.coverage.requested_end)}
                      </p>
                    </div>

                    <div className="rounded-xl border border-black/[0.06] bg-black/[0.015] p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-black/35">
                        Evidence period
                      </p>

                      <p className="mt-1 text-xs font-medium text-black/70">
                        {result.research.coverage.evidence_start
                          ? formatDate(result.research.coverage.evidence_start)
                          : "No evidence"}
                        {" → "}
                        {result.research.coverage.evidence_end
                          ? formatDate(result.research.coverage.evidence_end)
                          : "No evidence"}
                      </p>
                    </div>

                    <div className="rounded-xl border border-black/[0.06] bg-black/[0.015] p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-black/35">
                        Observations
                      </p>

                      <p className="mt-1 text-xs font-medium text-black/70">
                        {result.research.coverage.observations.toLocaleString()}
                      </p>
                    </div>

                  </div>


                  <div className="mt-5 max-h-[420px] space-y-2 overflow-auto pr-1">

                    {result.research.evidence.map((item, index) => (

                      <div

                        key={`${item.description}-${index}`}

                        className="rounded-xl border border-black/[0.06] px-4 py-3"

                      >

                        <div className="flex items-center justify-between gap-3">

                          <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-black/40">

                            {item.source}

                          </span>


                          <span className="text-[10px] text-black/30">

                            {formatDate(item.description.slice(-10))}

                          </span>

                        </div>


                        <p className="mt-2 text-xs leading-5 text-black/55">

                          {item.description}

                        </p>

                      </div>

                    ))}

                  </div>

                </div>


                <div className="rounded-2xl border border-amber-200/70 bg-amber-50/50 p-6">

                  <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-amber-800/60">

                    Limitations

                  </p>


                  <div className="mt-4 space-y-3">

                    {result.research.limitations.map((limitation) => (

                      <p

                        key={limitation}

                        className="text-xs leading-5 text-amber-900/65"

                      >

                        {limitation}

                      </p>

                    ))}

                  </div>

                </div>

              </div>

            </div>


            <footer className="mt-10 border-t border-black/[0.07] py-7 text-[10px] leading-5 text-black/30">

              QuantMind Research Workspace · Evidence before trust · Market data

              and analysis are provided for research purposes.

            </footer>

          </section>

        )}


        {!result && !loading && (

          <div className="mx-auto mt-20 max-w-3xl text-center">

            <div className="grid grid-cols-3 gap-3">

              <Feature label="Market data" />

              <Feature label="AI analysis" />

              <Feature label="Evidence graph" />

            </div>

          </div>

        )}

      </div>

    </main>

  );

}


function Metric({ label, value }: { label: string; value: string }) {

  return (

    <div>

      <p className="text-[10px] uppercase tracking-[0.12em] text-black/30">

        {label}

      </p>

      <p className="mt-1 text-sm font-medium">{value}</p>

    </div>

  );

}


function Coverage({ label, value }: { label: string; value: string }) {

  return (

    <div className="flex items-center justify-between border-b border-black/[0.06] pb-4 last:border-0">

      <span className="text-xs text-black/40">{label}</span>

      <span className="font-mono text-xs text-black/70">{value}</span>

    </div>

  );

}


function AnalysisList({

  title,

  items,

}: {

  title: string;

  items: string[];

}) {

  if (!items.length) return null;


  return (

    <div>

      <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-black/30">

        {title}

      </p>


      <div className="mt-3 space-y-2">

        {items.map((item) => (

          <div

            key={item}

            className="flex gap-3 text-sm leading-6 text-black/65"

          >

            <span className="mt-[9px] h-1 w-1 shrink-0 rounded-full bg-black/30" />

            <span>{item}</span>

          </div>

        ))}

      </div>

    </div>

  );

}


function Feature({ label }: { label: string }) {

  return (

    <div className="rounded-xl border border-black/[0.07] bg-white px-4 py-5 text-xs text-black/45">

      {label}

    </div>

  );

}