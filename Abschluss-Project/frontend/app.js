const express = require("express");
const AWS = require("aws-sdk");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;

// Configure AWS SDK
AWS.config.update({
  region: "your-region", // z.B. 'us-east-1'
  accessKeyId: "your-access-key-id",
  secretAccessKey: "your-secret-access-key",
});

const dynamoDb = new AWS.DynamoDB.DocumentClient();

app.use(bodyParser.json());

app.post("/api/attendance", (req, res) => {
  const { name, week, mondayStart, mondayEnd } = req.body;
  // Add similar fields for other days

  const params = {
    TableName: "AttendanceTable",
    Item: {
      name: name,
      week: week,
      mondayStart: mondayStart,
      mondayEnd: mondayEnd,
      // Add similar fields for other days
    },
  };

  dynamoDb.put(params, (err, data) => {
    if (err) {
      console.error("Error saving data to DynamoDB", err);
      res.status(500).send(err);
    } else {
      res.status(200).json({ success: true, data: data });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
