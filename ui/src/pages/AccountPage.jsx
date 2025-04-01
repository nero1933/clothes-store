import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

const AccountPage = () => {
    return (
      <>
          <Header/>
              <ul>
                  <li>Addresses</li>
                  <li>Orders</li>
                  <li>Reviews</li>
                  <li>Logout</li>
              </ul>
          <Footer/>
      </>
  );
};

export default AccountPage;