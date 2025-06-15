'use client';

import QuestionForm from '@/components/QuestionForm';
import Layout from '@/components/Layout';

export default function AskQuestionPage() {
  return (
    <Layout>
      <div className="p-6">
        <QuestionForm />
      </div>
    </Layout>
  );
}
