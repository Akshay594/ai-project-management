import React from 'react';

const RiskDisplay = ({ messages }) => {
  const assistantMessage = messages.find((message) => message.role === 'assistant');

  if (!assistantMessage) {
    return null;
  }

  const data = JSON.parse(assistantMessage.content);

  return (
    <div className="mt-6">
      <h2 className="text-2xl font-bold mb-4">Risks</h2>
      <div className="space-y-4">
        {data.risks.map((risk, index) => (
          <div key={index} className="p-4 border rounded-lg bg-red-100">
            <h3 className="text-xl font-semibold">{risk.category}</h3>
            <p>{risk.description}</p>
          </div>
        ))}
      </div>
      <h2 className="text-2xl font-bold mt-6 mb-4">Mitigation Actions</h2>
      <ul className="list-disc list-inside">
        {data.mitigation_actions.map((action, index) => (
          <li key={index}>{action}</li>
        ))}
      </ul>
    </div>
  );
};

export default RiskDisplay;
