// Sample data utilities for the Stack Overflow clone

// Simple seedable random number generator for deterministic results
function seededRandom(seed: number) {
  let x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

export interface User {
  id: number;
  name: string;
  reputation: number;
  avatar: string;
  location?: string;
  badges: {
    gold: number;
    silver: number;
    bronze: number;
  };
}

export interface Question {
  id: number;
  title: string;
  content: string;
  author: User;
  votes: number;
  views: string | number;
  asked: string;
  modified: string;
  tags: string[];
  answers: Answer[];
}

export interface Answer {
  id: number;
  content: string;
  author: User;
  votes: number;
  isAccepted: boolean;
  answered: string;
}

export const sampleUsers: User[] = [
  {
    id: 1,
    name: "Max A.",
    reputation: 4892,
    avatar: "https://www.gravatar.com/avatar/9a6a8a571b7c47685b3ee15cfbd1e3dc?s=64&d=identicon&r=PG",
    location: "San Francisco, CA",
    badges: { gold: 6, silver: 30, bronze: 29 }
  },
  {
    id: 2,
    name: "Bozho",
    reputation: 17430,
    avatar: "https://www.gravatar.com/avatar/sample1?s=64&d=identicon&r=PG",
    location: "Sofia, Bulgaria",
    badges: { gold: 15, silver: 45, bronze: 78 }
  },
  {
    id: 3,
    name: "John Developer",
    reputation: 8543,
    avatar: "https://www.gravatar.com/avatar/sample2?s=64&d=identicon&r=PG",
    location: "London, UK",
    badges: { gold: 3, silver: 18, bronze: 42 }
  }
];

export const sampleTags = [
  "javascript", "typescript", "react", "nextjs", "nodejs",
  "python", "java", "c#", "php", "go", "rust", "swift",
  "html", "css", "sql", "mongodb", "postgresql", "mysql",
  "docker", "kubernetes", "aws", "azure", "gcp"
];

export const generateSampleQuestion = (id: number): Question => {
  const titles = [
    "How to implement authentication in React?",
    "What's the difference between var, let, and const in JavaScript?",
    "How to handle state management in large React applications?",
    "Best practices for API design in Node.js",
    "How to optimize database queries in PostgreSQL?",
    "Understanding closure in JavaScript",
    "How to implement JWT authentication?",
    "What are React hooks and how to use them?",
    "How to deploy a Next.js application to Vercel?",
    "Understanding async/await in JavaScript"
  ];

  const contents = [
    "I'm building a React application and need to implement user authentication. What are the best practices for handling user login, logout, and protecting routes?",
    "I'm confused about the differences between var, let, and const in JavaScript. Can someone explain when to use each one and what the scope differences are?",
    "As my React application grows, managing state becomes more complex. What are the recommended patterns for state management in large applications?",
    "I'm designing a REST API in Node.js and want to follow best practices. What are the key principles I should follow for a well-designed API?",
    "My PostgreSQL queries are running slowly on large datasets. What are some techniques to optimize query performance?",
    "I keep hearing about closures in JavaScript but don't fully understand them. Can someone explain what they are and provide practical examples?",
    "I need to implement JWT-based authentication in my web application. What's the proper way to handle JWT tokens on both client and server side?",
    "React hooks seem powerful but I'm not sure how to use them effectively. Can someone explain the most commonly used hooks with examples?",
    "I've built a Next.js application and want to deploy it to Vercel. What's the deployment process and are there any gotchas I should know about?",
    "I'm learning about asynchronous JavaScript and async/await syntax. How does it work and when should I use it instead of promises?"
  ];

  const tags = [
    ["react", "authentication", "javascript"],
    ["javascript", "variables", "scope"],
    ["react", "state-management", "redux"],
    ["node.js", "api", "rest", "express"],
    ["postgresql", "database", "performance"],
    ["javascript", "closures", "functions"],
    ["jwt", "authentication", "security"],
    ["react", "hooks", "usestate", "useeffect"],
    ["next.js", "vercel", "deployment"],
    ["javascript", "async-await", "promises"]
  ];

  const titleIndex = (id - 1) % titles.length;
  const contentIndex = (id - 1) % contents.length;
  const tagIndex = (id - 1) % tags.length;

  const votes = Math.floor(seededRandom(id * 1000) * 50) + 1;
  const viewCount = Math.floor(seededRandom(id * 2000) * 10000) + 100;
  const answerCount = Math.floor(seededRandom(id * 3000) * 5);

  const answers: Answer[] = [];
  for (let i = 0; i < answerCount; i++) {
    answers.push(generateSampleAnswer(i + 1));
  }

  return {
    id,
    title: titles[titleIndex],
    content: contents[contentIndex],
    author: {
      id: id + 1000, // Generate a unique user ID
      name: `User${id}`,
      reputation: Math.floor(seededRandom(id * 4000) * 10000) + 100,
      avatar: `https://www.gravatar.com/avatar/user${id}?s=64&d=identicon&r=PG`,
      badges: {
        gold: Math.floor(seededRandom(id * 5000) * 10),
        silver: Math.floor(seededRandom(id * 6000) * 30),
        bronze: Math.floor(seededRandom(id * 7000) * 50)
      }
    },
    votes,
    views: viewCount > 1000 ? `${Math.floor(viewCount / 1000)}k` : viewCount.toString(),
    asked: `${Math.floor(seededRandom(id * 8000) * 24)} hours ago`,
    modified: `${Math.floor(seededRandom(id * 9000) * 12)} hours ago`,
    tags: tags[tagIndex],
    answers
  };
};

export const generateSampleAnswer = (id: number): Answer => {
  const contents = [
    "<p>Here's a comprehensive solution to your problem:</p><p>You can use the following approach...</p>",
    "<p>I recommend this solution:</p><ul><li>First step</li><li>Second step</li><li>Third step</li></ul>",
    "<p>This is a common issue. The best way to handle it is...</p>",
    "<p>Based on my experience, I would suggest:</p><p>This approach has worked well for me.</p>"
  ];

  const randomUser = sampleUsers[Math.floor(seededRandom(id * 10000) * sampleUsers.length)];

  return {
    id,
    content: contents[Math.floor(seededRandom(id * 11000) * contents.length)],
    author: randomUser,
    votes: Math.floor(seededRandom(id * 12000) * 50),
    isAccepted: seededRandom(id * 13000) > 0.7,
    answered: `${Math.floor(seededRandom(id * 14000) * 48)} hours ago`
  };
};

export const generateSampleQuestions = (count: number): Question[] => {
  const questions: Question[] = [];
  for (let i = 1; i <= count; i++) {
    questions.push(generateSampleQuestion(i));
  }
  return questions;
};
