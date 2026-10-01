import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [articles, setArticles] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSource, setSelectedSource] = useState("All");
  const [selectedType, setSelectedType] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [subscribeMsg, setSubscribeMsg] = useState("");
  const [subscribing, setSubscribing] = useState(false);
  const API_URL = "https://ai-news-aggregator-2-calg.onrender.com" 

  // ================================
  // FETCH NEWS FROM FASTAPI
  // ================================

  useEffect(() => {
    console.log("Fetching news from..");

    fetch(`${API_URL}/news`)
      .then((response) => {
        console.log("Response status:", response.status);

        if (!response.ok) {
          throw new Error("Failed to fetch news");
        }

        return response.json();
      })
      .then((data) => {
        console.log("BACKEND DATA:", data);
        console.log("ARTICLE COUNT:", data.articles.length);

        setArticles(data.articles);
        setLoading(false);
      })
      .catch((error) => {
        console.error("BACKEND ERROR:", error);

        setError(error.message);
        setLoading(false);
      });
  }, []);

const handleSubscribe = () => {
  if (!email.trim()) {
    setSubscribeMsg("Please enter an email.");
    return;
  }

  setSubscribing(true);
  setSubscribeMsg("");

  fetch(`${API_URL}/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email.trim() }),
  })
    .then((response) => response.json())
    .then((data) => {
      setSubscribeMsg(
        data.success
          ? "Subscribed! You'll get daily AI news in your inbox."
          : "You're already subscribed."
      );
      setEmail("");
    })
    .catch(() => {
      setSubscribeMsg("Something went wrong. Try again.");
    })
    .finally(() => {
      setSubscribing(false);
    });
};
  // ================================
  // FILTER NEWS
  // ================================

  const filteredArticles = articles.filter((article) => {

    const title = article.title || "";

    const matchesSearch = title
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesSource =
      selectedSource === "All" ||
      article.source === selectedSource;

    const matchesType =
      selectedType === "All" ||
      article.source_type === selectedType;

    return (
      matchesSearch &&
      matchesSource &&
      matchesType
    );
  });


  // ================================
  // SOURCES
  // ================================

  const sources = [
    "All",
    ...new Set(
      articles
        .map((article) => article.source)
        .filter(Boolean)
    ),
  ];


  // ================================
  // LOADING
  // ================================

  if (loading) {
    return (
      <div className="app">
        <h1>AI News Aggregator</h1>
        <h2>Loading news...</h2>
      </div>
    );
  }


 
  // ================================
  // ERROR
  // ================================

  if (error) {
    return (
      <div className="app">
        <h1>AI News Aggregator</h1>

        <h2>
          Error: {error}
        </h2>
      </div>
    );
  }
  

  // ================================
  // MAIN UI
  // ================================

  return (
    <div className="app">

      {/* HEADER */}

      <header>
        <h1>
          AI News Aggregator
        </h1>

        <p>
          Latest Artificial Intelligence News
        </p>
      </header>
      <div className="subscribe">
  <input
    type="email"
    placeholder="Enter your email for daily digest"
    value={email}
    onChange={(event) => setEmail(event.target.value)}
  />

  <button onClick={handleSubscribe} disabled={subscribing}>
    {subscribing ? "Subscribing..." : "Subscribe"}
  </button>

  {subscribeMsg && <p className="subscribe-msg">{subscribeMsg}</p>}
</div>

      {/* SEARCH + FILTERS */}

      <div className="controls">

        <input
          type="text"
          placeholder="Search AI news..."
          value={searchTerm}
          onChange={(event) =>
            setSearchTerm(event.target.value)
          }
        />


        <select
          value={selectedSource}
          onChange={(event) =>
            setSelectedSource(event.target.value)
          }
        >

          {sources.map((source) => (
            <option
              key={source}
              value={source}
            >
              {source}
            </option>
          ))}

        </select>


        <select
          value={selectedType}
          onChange={(event) =>
            setSelectedType(event.target.value)
          }
        >

          <option value="All">
            All Types
          </option>

          <option value="article">
            Articles
          </option>

          <option value="video">
            Videos
          </option>

          <option value="reddit">
            Reddit
          </option>

        </select>

      </div>


      {/* ARTICLE COUNT */}

      <div className="count">

        Showing{" "}
        <strong>
          {filteredArticles.length}
        </strong>{" "}

        of{" "}

        <strong>
          {articles.length}
        </strong>{" "}

        articles

      </div>


      {/* NEWS GRID */}

      <main className="news-grid">

        {filteredArticles.map(
          (article, index) => (

            <article
              className="news-card"
              key={
                article.url || index
              }
            >

              <div className="source">
                {article.source}
              </div>


              <h2>
                {article.title}
              </h2>


              {article.description && (
                <p>
                  {article.description}
                </p>
              )}


              <div className="article-info">

                <span>
                  {article.source_type}
                </span>

                <span>
                  {article.published_at
                    ? new Date(
                        article.published_at
                      ).toLocaleDateString()
                    : ""}
                </span>

              </div>


              {article.url && (
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Read More →
                </a>
              )}

            </article>

          )
        )}

      </main>


      {/* NO RESULTS */}

      {filteredArticles.length === 0 && (
        <div className="message">
          No articles match your filters.
        </div>
      )}

    </div>
  );
}

export default App;