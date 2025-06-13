import QuestionDetail from "@/components/QuestionDetail";

interface QuestionPageProps {
  params: Promise<{
    id: string;
    slug: string;
  }>;
}

export default async function QuestionDetailPage({ params }: QuestionPageProps) {
  const { id } = await params;
  // Note: slug parameter is available for SEO but not used in this implementation
  
  // Sample data for the specific servlet question
  const questionData = {
    id: parseInt(id),
    title: "What are the differences between Servlet 2.5 and 3?",
    content: "I'm rolling J2EE code that adheres to Servlet 2.5 and I'm wondering what are the major differences between 2.5 and 3. Pointers to official Sun docs and personal experiences are most appreciated.\n\nIf I shouldn't be concerning myself with 3 for the time being, just say so. Thanks!",
    author: {
      name: "Max A.",
      reputation: 4892,
      avatar: "https://www.gravatar.com/avatar/9a6a8a571b7c47685b3ee15cfbd1e3dc?s=64&d=identicon&r=PG",
      badges: {
        gold: 6,
        silver: 30,
        bronze: 29
      }
    },
    votes: 99,
    views: "67k",
    asked: "15 years, 7 months ago",
    modified: "8 years, 5 months ago",
    tags: ["java", "servlets", "jakarta-ee"],
    answers: [
      {
        id: 18187372,
        content: `<p><strong>UPDATE</strong></p>

<p>Just as an update and to be more explicit, these are the main differences between servlets 2.5 and 3 (I'm not trying to be exhaustive, I'm just mentioning the most interesting parts):</p>

<h2>Annotations to declare servlets, filters and listeners (ease of development)</h2>

<p>In servlets 2.5, to declare a servlet with one init parameter you need to add this to <strong>web.xml</strong>:</p>

<pre><code>&lt;servlet&gt;
    &lt;servlet-name&gt;myServlet&lt;/servlet-name&gt;
    &lt;servlet-class&gt;my.server.side.stuff.MyAwesomeServlet&lt;/servlet-class&gt;
    &lt;init-param&gt;
        &lt;param-name&gt;configFile&lt;/param-name&gt;
        &lt;param-value&gt;config.xml&lt;/param-value&gt;
    &lt;/init-param&gt;
&lt;/servlet&gt;

&lt;servlet-mapping&gt;
    &lt;servlet-name&gt;myServlet&lt;/servlet-name&gt;
    &lt;url-pattern&gt;/path/to/my/servlet&lt;/url-pattern&gt;
&lt;/servlet-mapping&gt;
</code></pre>

<p>In servlets 3, <strong>web.xml</strong> is optional and you can use annotations instead of XML. The same example:</p>

<pre><code>@WebServlet(name="myServlet",
    urlPatterns={"/path/to/my/servlet"},
    initParams={@InitParam(name="configFile", value="config.xml")})
public class MyAwesomeServlet extends HttpServlet { ... }
</code></pre>`,
        author: {
          name: "Bozho",
          reputation: 17430,
          avatar: "https://www.gravatar.com/avatar/sample1?s=64&d=identicon&r=PG",
          badges: {
            gold: 15,
            silver: 45,
            bronze: 78
          }
        },
        votes: 158,
        isAccepted: true,
        answered: "Aug 12, 2013 at 8:45"
      },
      {
        id: 1638867,
        content: `<p>The main differences include:</p>

<ul>
<li><strong>Annotations support:</strong> Servlet 3.0 introduced annotations like @WebServlet, @WebFilter, and @WebListener</li>
<li><strong>Pluggability:</strong> Web fragments allow modular configuration</li>
<li><strong>Asynchronous processing:</strong> Support for async servlets</li>
<li><strong>File upload:</strong> Built-in support for multipart/form-data</li>
</ul>

<p>These changes make development much easier and reduce the need for XML configuration.</p>`,
        author: {
          name: "John Developer",
          reputation: 8543,
          avatar: "https://www.gravatar.com/avatar/sample2?s=64&d=identicon&r=PG",
          badges: {
            gold: 3,
            silver: 18,
            bronze: 42
          }
        },
        votes: 45,
        isAccepted: false,
        answered: "Oct 28, 2009 at 18:15"
      }
    ]
  };

  return (
    <div className="bg-white min-h-screen">
      <QuestionDetail question={questionData} />
    </div>
  );
}
