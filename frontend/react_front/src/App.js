import './App.css';
//import NaviBar from "./reactComponent/naviBar"
import GetAuthor from "./reactComponent/getAuthor.jsx"
import GetBook from "./reactComponent/getBook.jsx"
import GetSearch from './reactComponent/getsearch';
import PutAuthor from './reactComponent/putAuthor';
import PutBook from './reactComponent/putBook';
import PostBook from './reactComponent/postBook';
import PostAuthor from './reactComponent/postAuthor';
import PostScrape from './reactComponent/postScrape';
import DeleteBook from './reactComponent/deleteBook';
import DeleteAuthor from './reactComponent/deleteAuthor';
import GetTopNBook from './reactComponent/getTopNBook';
import GetTopNauthor from './reactComponent/getTopNAuthor';

/**
 * The app wrapper
 */
function App() {
  return (
    <div>
      <div className="header">
        <h1>Assignment2 web app</h1>
        <p>Jincheng Liu</p>
      </div>
      <div className= "entireWrapper">
        <GetAuthor/>
        <GetBook/>
        <GetSearch/>
        <PutBook/>
        <PutAuthor/>
        <PostBook/>
        <PostAuthor/>
        <PostScrape/>
        <DeleteBook/>
        <DeleteAuthor/>
        <GetTopNBook/>
        <GetTopNauthor/>
      </div>
    </div>
    );
}

export default App;