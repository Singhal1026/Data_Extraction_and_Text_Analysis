# Data_Extraction_and_Text_Analysis

<h3>OBJECTIVE</h3>
<p>To scrape data from various URLs and perform analysis on text
content to extract information such as positive score, word count,
sentence count, syllable count, avg sentence length, etc.</p>

<h3>APPROACH</h3>
<ol>
  <li><strong>Web Scrapping</strong>
    <ul>
    <li> Use Beautiful Soup to scrape data from each URL.</li>
    <li> Retrieve text content from scraped data.</li>
    </ul>
  </li>
  <li> <strong> Data Storage </strong>
    <ul>
      <li> Store the scrapped text content in local Directory using ‘os module’</li>
    </ul>
  </li>
  <li> <strong> Retrieve Given Data </strong>
    <ul>
      <li> Data like stop words is retrieved and stored in a common array for further preprocessing.</li>
      <li>Output.xlsx is retrieved as a DataFrame named as output. </li>
    </ul>
  </li>
  <li> <strong> Preprocessing </strong>
    <ul>
      <li> Scraped data is preprocessed like punctuation removal, stopword removal.</li>
    </ul>
  </li>
  <li> <strong> Parameter Calculation </strong>
    <ul>
      <li> Required features are Calculated for each URL. </li>
      <li> Also make sure which parameters or features require preprocessing step or not. </li>
    </ul>
  </li>
  <li> <strong> Results </strong>
    <ul>
      <li> These calculated data is stored in output DataFrame.</li>
      <li> Now this DataFrame is converted to comma separated File(csv) File.</li>
    </ul>
  </li>
</ol>

<h3> Dependencies Required </h3>
<ul>
  <li> <strong>requests:</strong> To make HTTP requests to fetch web pages. </li>
  <li> <strong>pandas:</strong> To create DataFrame for storing output. </li>
  <li> <strong>os:</strong> To fetch data from our file system. </li>
  <li> <strong>beautifulsoup:</strong> To scrap web pages. </li>
  <li> <strong>nltk: </strong>To perform preprocessing tasks on data. </li>
  <li> <strong>re: </strong>re is for Regular Expression. </li>
  <li> <strong>string: </strong> to perform some preprocessing. </li>
  <li> <strong>openpyxl </strong> </li>
  <li> <strong>lxml </strong> </li>
</ul>
