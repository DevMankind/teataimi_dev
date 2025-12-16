SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `teataimi`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Seller','Customer') DEFAULT 'Customer',
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `phone`, `password`, `role`, `address`, `created_at`) VALUES
(1, 'Admin001', 'admin@tetaimi.com', '01119111568', 'Admin001', 'Admin', NULL, '2025-11-02 08:43:01'),
(2, 'Admin User', 'admin@teataimi.com', '0000000000', 'admin123', 'Admin', 'Admin Office', NOW()),
(3, 'Testing', 'test123@gmail.com', '0189161789', 'Testing123', 'Customer', '', '2025-11-02 08:43:01'),
(4, 'Demo Customer', 'demo@teataimi.com', '0123456789', 'demo123', 'Customer', '123 Demo Street, Penang', NOW());

-- --------------------------------------------------------

--
-- Table structure for table `products`
-- I have added 'category' and 'image_url' here to match your HTML needs
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 100,
  `category` varchar(50) DEFAULT 'General',
  `image_url` varchar(255) DEFAULT 'images/default.png',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
-- OLD DATA (IDs 2001-2003) + NEW BAKERY DATA (IDs Auto-generated)
--

INSERT INTO `products` (`product_id`, `product_name`, `description`, `price`, `stock`, `category`, `image_url`) VALUES
-- Existing Items
(2001, 'Nutty Brownies', 'Rich, fudgy brownies topped with roasted nuts.', 60.00, 5, 'Brownies', 'images/brownies.png'),
(2002, 'Cadbury Brownies', 'Signature brownies smothered in Cadbury chocolate.', 52.00, 4, 'Brownies', 'images/nb.png'),
(2003, 'Brownies with Lotus Biscoff', 'Brownies topped with Lotus Biscoff spread.', 50.00, 4, 'Brownies', 'images/lbb.png'),

-- NEW MENU ITEMS (Cheesecakes)
(NULL, 'Mini Burnt Cheesecake', '12 pcs of creamy, velvety Basque-style cheesecake.', 45.00, 50, 'Cheesecake', 'images/mbcc.png'),
(NULL, 'Lotus Biscoff Mini Burnt Cheesecake', '12 pcs of creamy cheesecake infused with Biscoff spread.', 50.00, 50, 'Cheesecake', 'images/lbccake.png'),
(NULL, 'Nutella Mini Burnt Cheesecake', '12 pcs of creamy cheesecake swirled with decadent, baked Nutella.', 50.00, 50, 'Cheesecake', 'images/ncc.png'),
(NULL, 'Mix Fruit Mini Burnt Cheesecake', '12 pcs of basque cheesecake topped with a mix of berries and fruits.', 55.00, 50, 'Cheesecake', 'images/mixfruitcc.png'),
(NULL, 'Mix Mini Burnt Cheesecake', 'A trio of signature velvety cheesecakes.', 50.00, 50, 'Cheesecake', 'images/mixcc.png'),

-- NEW MENU ITEMS (Brownies)
(NULL, 'Brownies', '9" of fudgy and chocolatey with a perfect crackly top.', 60.00, 50, 'Brownies', 'images/brownies.png'),
(NULL, 'Lotus Biscoff Brownies', '9" of fudgy brownies topped with creamy Biscoff spread.', 70.00, 50, 'Brownies', 'images/lbb.png'),
(NULL, 'Nutella Brownies', '9" of gooey brownies marbled throughout with warm Nutella.', 70.00, 50, 'Brownies', 'images/nb.png'),
(NULL, 'Brownies Cupcake', '6 pcs of fudgy, dense brownie baked in a cupcake form.', 30.00, 50, 'Brownies', 'images/bc.png'),
(NULL, 'Mix Brownies', 'A box with Biscoff-topped brownies and Nutella-swirled brownies.', 70.00, 50, 'Brownies', 'images/mixbs.png'),

-- NEW MENU ITEMS (Cheese Tart)
(NULL, 'Lotus Biscoff Cheese Tart', '25 pcs of buttery tart shell, creamy cheese filling.', 50.00, 50, 'Cheese Tart', 'images/lbc.png'),
(NULL, 'Nutella Cheese Tart', '25 pcs of delicate tart filled with creamy cheese.', 50.00, 50, 'Cheese Tart', 'images/nct.png'),
(NULL, 'Blueberry Cheese Tart', '25 pcs of buttery tart with creamy cheese and blueberry.', 50.00, 50, 'Cheese Tart', 'images/bct.png'),
(NULL, 'Matcha Cheese Tart', '25 pcs of crisp tart shell with creamy cheese and matcha.', 50.00, 50, 'Cheese Tart', 'images/matchact.png'),
(NULL, 'Mix Cheese Tart', 'A box of cheese tarts with 4 flavors.', 50.00, 50, 'Cheese Tart', 'images/mixct.png'),

-- NEW MENU ITEMS (Cakesicles)
(NULL, 'Cakesicles', '6 pcs of cake and frosting, molded like a popsicle.', 60.00, 50, 'Cakesicles', 'images/cakesicles.png');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `delivery_date` date DEFAULT NULL,
  `status` enum('Pending','In Progress','Completed','Delivered') DEFAULT 'Pending',
  `total_amount` decimal(10,2) DEFAULT 0.00,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `order_date`, `delivery_date`, `status`, `total_amount`) VALUES
(12200, 3, '2025-11-02 08:56:57', '2025-11-05', 'Pending', 120.00),
(12201, 3, '2025-11-02 08:56:57', '2025-11-06', 'Pending', 52.00);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `product_id`, `quantity`, `price`) VALUES
(101, 12200, 2001, 2, 120.00),
(102, 12201, 2002, 1, 52.00);

-- --------------------------------------------------------

--
-- Optional: Table structure for table `product_images`
-- Keeps this empty or for multiple images per product support
--

CREATE TABLE `product_images` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_main` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`image_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Adjust AUTO_INCREMENT Values
--
ALTER TABLE `users` AUTO_INCREMENT = 5;
ALTER TABLE `orders` AUTO_INCREMENT = 12202;
ALTER TABLE `order_items` AUTO_INCREMENT = 103;
ALTER TABLE `products` AUTO_INCREMENT = 3000;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;