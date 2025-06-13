# Stack Overflow Clone

A Stack Overflow clone built with Next.js, TypeScript, and Tailwind CSS. This project replicates the core functionality and design of Stack Overflow's Q&A interface.

## Features

### Implemented
- **Question Detail Page**: Full question view with voting, answers, and user information
- **Header Navigation**: Search functionality, user profile, notifications
- **Sidebar Navigation**: Links to main sections (Questions, Tags, Users, etc.)
- **Questions List**: Browse all questions with filters and pagination
- **Tags Page**: View and filter programming tags
- **Users Page**: Browse user profiles with reputation and badges
- **Ask Question**: Form to post new questions
- **Collectives**: Specialized communities for technologies
- **Responsive Design**: Mobile-friendly layout

### Question Detail Features
- ✅ Question voting (up/down arrows)
- ✅ Answer voting and acceptance
- ✅ User profiles with reputation and badges
- ✅ Tags display
- ✅ Question metadata (asked date, views, etc.)
- ✅ Multiple answers with rich content
- ✅ Action buttons (Share, Edit, Follow, Flag)

### UI Components
- ✅ Header with Stack Overflow branding
- ✅ Search bar
- ✅ User avatar and stats
- ✅ Notification indicators
- ✅ Sidebar with navigation
- ✅ Teams promotion section
- ✅ Collectives section

## Technology Stack

- **Frontend**: Next.js 15 with TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Development**: ESLint, PostCSS

## Project Structure

```
src/
├── app/                    # Next.js 13+ App Router
│   ├── ask/               # Ask Question page
│   ├── collectives/       # Collectives page
│   ├── questions/         # Questions listing page
│   ├── tags/              # Tags page
│   ├── users/             # Users page
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page (Question Detail)
├── components/
│   ├── Header.tsx         # Top navigation
│   ├── Sidebar.tsx        # Left sidebar navigation
│   └── QuestionDetail.tsx # Main question component
```

## Routes

- `/` - Home page showing a sample question detail
- `/questions` - Browse all questions
- `/tags` - View and filter tags
- `/users` - Browse user profiles
- `/ask` - Ask a new question
- `/collectives` - View technology collectives

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Run the development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Sample Data

The application currently uses hardcoded sample data based on the original Stack Overflow question about "Servlet 2.5 vs 3" differences. This includes:
- Question content and metadata
- Sample answers with code examples
- User profiles with realistic reputation and badge counts
- Tags and other related information

## Future Enhancements

### Planned Features
- **User Authentication**: Login/signup functionality
- **Database Integration**: Real data persistence
- **Question CRUD**: Create, edit, delete questions
- **Answer System**: Post and manage answers
- **Voting System**: Functional up/down voting
- **Search**: Advanced search with filters
- **Notifications**: Real-time updates
- **User Profiles**: Complete user management
- **Badge System**: Achievement tracking
- **Comment System**: Question and answer comments
- **Markdown Editor**: Rich text editing for posts

### Additional Pages
- **User Profile**: Individual user pages
- **Question Edit**: Edit existing questions
- **Admin Panel**: Moderation tools
- **Help Center**: Documentation and guides
- **Jobs Board**: Developer job listings
- **Teams**: Private Q&A for organizations

## Contributing

This is a learning project demonstrating Next.js and modern web development practices. Feel free to:
- Report issues or bugs
- Suggest new features
- Submit pull requests
- Use as a reference for your own projects

## License

This project is for educational purposes. Stack Overflow is a trademark of Stack Exchange Inc.
