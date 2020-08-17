-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 16, 2020 at 10:30 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_pigeon_infinity`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `pass`, `name`) VALUES
(1, 'xian@xian.com', '1807215e72492dd5fa118a6c6f620af0', 'Xian');

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `id` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 NOT NULL,
  `picture` varchar(255) CHARACTER SET utf8 NOT NULL,
  `para1` text CHARACTER SET utf8 NOT NULL,
  `para2` text CHARACTER SET utf8 NOT NULL,
  `auth` varchar(255) CHARACTER SET utf8 NOT NULL,
  `timedate` varchar(255) NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`id`, `title`, `picture`, `para1`, `para2`, `auth`, `timedate`) VALUES
(1, 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..', 'abc.jpg', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sapien odio, convallis eu arcu quis, venenatis hendrerit augue. Sed laoreet aliquam justo mollis hendrerit. In lacinia purus sed quam molestie, non dignissim ex rhoncus. Proin aliquam consectetur tellus, sit amet iaculis mi viverra at. Curabitur feugiat fermentum risus, a rhoncus velit ullamcorper eget. Aenean rhoncus commodo sollicitudin. Pellentesque at feugiat erat. Nam fermentum feugiat arcu, vitae consequat ante ultrices egestas. Nam gravida felis metus, at porttitor enim tempor ac. Suspendisse a dolor metus. ', 'Mauris luctus risus mi, vel rutrum nisi sollicitudin nec. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent id facilisis augue. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris volutpat sagittis diam, at tristique nulla suscipit a. In quis rutrum massa. In tempus eleifend purus quis imperdiet. Ut malesuada et nisl nec aliquet. Donec sit amet erat eget ligula sodales pulvinar non sit amet tellus. Quisque sed nibh eget tortor sagittis sagittis ut a nisi. Aliquam magna elit, molestie et porttitor vitae, volutpat id diam. Aenean rhoncus, mi tempus luctus faucibus, magna tortor viverra turpis, eget maximus tortor velit sit amet est. Mauris aliquet a nibh nec fermentum. Proin odio nisl, posuere vel laoreet id, varius sed urna. ', 'Xian', '14-Aug-2020'),
(2, 'test', '1597519904111.jpg', 'asda', 'sdasd', 'Xian', '2020-08-16 01:31:44'),
(3, 'asd', '1597520085583.jpg', 'asd', 'asd', 'Xian', '2020-08-16 01:34:45'),
(4, 'dwqeqwe', '1597520163451.jpg', 'qwewqeqweqwe', 'qwedqweqweqwe', 'Xian', '2020-08-16 01:36:03');

-- --------------------------------------------------------

--
-- Table structure for table `auctionevent`
--

CREATE TABLE `auctionevent` (
  `AuctionID` int(11) NOT NULL,
  `AuctionName` varchar(255) CHARACTER SET utf8 NOT NULL,
  `AuctionDetails` varchar(255) CHARACTER SET utf8 NOT NULL,
  `TotalPigeon` int(11) NOT NULL,
  `AuctionStart` varchar(255) CHARACTER SET utf8 NOT NULL,
  `AuctionEnd` varchar(255) CHARACTER SET utf8 NOT NULL,
  `MainPicture` varchar(255) CHARACTER SET utf8 NOT NULL,
  `Currency` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT 'BDT'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auctionevent`
--

INSERT INTO `auctionevent` (`AuctionID`, `AuctionName`, `AuctionDetails`, `TotalPigeon`, `AuctionStart`, `AuctionEnd`, `MainPicture`, `Currency`) VALUES
(13, 'Upcomming auction', '4563453212', 1, '2020-09-05 12:12:00', '2020-09-26 00:12:00', '1597002862216.jpg', 'BDT'),
(14, 'running auction', 'asdasd', 1, '2020-08-10 02:00:00', '2020-10-27 02:00:00', '1597003136879.jpg', 'BDT'),
(15, 'Faruk bhaiyer auction', 'Faruk bhaiyer auction Faruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFaruk bhaiyer auctionFa', 5, '2020-08-10 01:00:00', '2020-08-15 23:00:00', '1597004728836.jpg', 'BDT');

-- --------------------------------------------------------

--
-- Table structure for table `bid`
--

CREATE TABLE `bid` (
  `BidID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `PigeonID` int(11) NOT NULL,
  `AuctionID` int(11) NOT NULL,
  `BidAmount` int(11) NOT NULL,
  `BidTimeDate` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bid`
--

INSERT INTO `bid` (`BidID`, `UserID`, `PigeonID`, `AuctionID`, `BidAmount`, `BidTimeDate`) VALUES
(50, 2, 13, 14, 6000, '2020-08-10 02:22:05'),
(51, 2, 13, 14, 6500, '2020-08-10 02:22:09'),
(52, 2, 13, 14, 7000, '2020-08-10 02:22:12'),
(53, 2, 13, 14, 7500, '2020-08-10 02:22:16'),
(54, 2, 13, 14, 8000, '2020-08-10 02:22:56'),
(55, 2, 14, 15, 1999, '2020-08-10 02:29:24'),
(56, 2, 15, 15, 3000, '2020-08-13 23:51:25'),
(57, 3, 15, 15, 3500, '2020-08-13 23:51:37'),
(58, 2, 15, 15, 4000, '2020-08-13 23:52:00'),
(59, 2, 15, 15, 10000, '2020-08-13 23:52:51'),
(60, 2, 18, 15, 2000, '2020-08-14 00:54:22'),
(61, 3, 18, 15, 2500, '2020-08-14 01:34:09'),
(62, 2, 18, 15, 3000, '2020-08-14 01:34:18'),
(63, 2, 13, 14, 8500, '2020-08-16 22:42:49'),
(64, 2, 13, 14, 9000, '2020-08-16 22:42:58'),
(65, 2, 13, 14, 9500, '2020-08-16 22:43:52'),
(66, 2, 13, 14, 10000, '2020-08-16 22:45:31'),
(67, 2, 13, 14, 11000, '2020-08-16 23:21:26'),
(68, 2, 13, 14, 12000, '2020-08-16 23:52:15');

-- --------------------------------------------------------

--
-- Table structure for table `highfancier`
--

CREATE TABLE `highfancier` (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `sub` varchar(255) CHARACTER SET utf8 NOT NULL,
  `moto` varchar(255) CHARACTER SET utf8 NOT NULL,
  `pic` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `highfancier`
--

INSERT INTO `highfancier` (`id`, `name`, `sub`, `moto`, `pic`) VALUES
(1, 'Xian', 'CEO Secret Developers', 'Good website, keep it up guys', 'xian.jpg'),
(2, 'Quamrul Hasan Dipu', 'Senior Citizen', 'Eat Sleep Race', 'vai.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `pigeon`
--

CREATE TABLE `pigeon` (
  `PigeonID` int(11) NOT NULL,
  `AuctionID` int(11) NOT NULL,
  `PigeonRing` varchar(255) CHARACTER SET utf8 NOT NULL,
  `PigeonName` varchar(255) CHARACTER SET utf8 NOT NULL,
  `Price` int(11) NOT NULL,
  `MainPic` varchar(255) CHARACTER SET utf8 NOT NULL,
  `AllPic` varchar(255) CHARACTER SET utf8 NOT NULL,
  `PigeonGender` varchar(255) CHARACTER SET utf8 NOT NULL,
  `LastBidderID` int(11) DEFAULT -1,
  `PigeonColor` varchar(255) NOT NULL,
  `FixedPrice` varchar(11) DEFAULT 'NO',
  `BreedBy` varchar(255) CHARACTER SET utf8 NOT NULL,
  `OfferBy` varchar(255) CHARACTER SET utf8 NOT NULL,
  `PigeonDetails` varchar(255) CHARACTER SET utf8 NOT NULL,
  `LastBidderName` varchar(255) CHARACTER SET utf8 DEFAULT '---',
  `StartTime` varchar(255) CHARACTER SET utf8 NOT NULL,
  `EndTime` varchar(255) CHARACTER SET utf8 NOT NULL,
  `vdoLink` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pigeon`
--

INSERT INTO `pigeon` (`PigeonID`, `AuctionID`, `PigeonRing`, `PigeonName`, `Price`, `MainPic`, `AllPic`, `PigeonGender`, `LastBidderID`, `PigeonColor`, `FixedPrice`, `BreedBy`, `OfferBy`, `PigeonDetails`, `LastBidderName`, `StartTime`, `EndTime`, `vdoLink`) VALUES
(12, 13, 'ring 1', 'adky Bird 222', 5600, '1597002913346.jpg', '[\'15970029133460.jpg\']', 'asdas', -1, 'dasdas', 'NO', 'asdasd', 'asdasd', 'asd', '---', '2020-09-05 12:12:00', '2020-09-26 00:12:00', NULL),
(13, 14, 'BAN 13-659222', 'Rocky Bird 222', 12000, '1597003168287.jpg', '[\'15970031682870.jpg\', \'15970031682871.jpg\']', 'Male', 2, 'Red', 'NO', 'Abir Hossain Xian', 'Haunted Loft', 'asd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd asd asd asasd', 'Abir Hossain Xian', '2020-08-10 02:00:00', '2020-10-27 02:00:00', NULL),
(14, 15, 'Pigeon ring no 1', 'name  1', 1999, '1597004911536.jpg', '[\'15970049115360.jpg\']', 'Male', 2, 'Red', 'NO', 'Faruk bhai', 'Faruk bhai', 'Faruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhai', 'Abir Hossain Xian', '2020-08-10 01:00:00', '2020-08-15 23:00:00', NULL),
(15, 15, 'Pigeon ring no 2', 'name 2', 10000, '1597004911603.jpg', '[\'15970049116030.jpg\', \'15970049116031.jpg\', \'15970049116032.jpg\']', 'Male', 2, 'pink', 'NO', 'Faruk bhai', 'Faruk bhai', 'Faruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk', 'Abir Hossain Xian', '2020-08-10 01:00:00', '2020-08-15 23:00:00', NULL),
(16, 15, 'Pigeon ring no 3', 'name 3', 500, '1597004911702.jpg', '[\'15970049117020.jpg\', \'15970049117021.jpg\']', 'Male', -1, 'yellow', 'NO', 'Faruk bhai', 'Faruk bhai', 'Faruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk', '---', '2020-08-10 01:00:00', '2020-08-15 23:00:00', NULL),
(17, 15, 'Pigeon ring no 4', 'name 4', 1500, '1597004911744.jpg', '[\'15970049117440.jpg\']', 'Male', -1, 'black', 'NO', 'Faruk bhai', 'Faruk bhai', 'Faruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk', '---', '2020-08-10 01:00:00', '2020-08-15 23:00:00', NULL),
(18, 15, 'Pigeon ring no 5', 'name 5', 3000, '1597004911788.jpg', '[\'15970049117880.jpg\', \'15970049117881.jpg\']', 'Female', 2, 'transparent', 'NO', 'Faruk bhai', 'Faruk bhai', 'Faruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk bhaiFaruk', 'Abir Hossain Xian', '2020-08-10 01:00:00', '2020-08-15 23:00:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `setting`
--

CREATE TABLE `setting` (
  `id` int(11) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `heading` varchar(255) NOT NULL,
  `headingpic` varchar(255) NOT NULL,
  `headinglink` varchar(255) NOT NULL,
  `page` varchar(255) NOT NULL,
  `column1` varchar(255) NOT NULL,
  `column2` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `setting`
--

INSERT INTO `setting` (`id`, `phone`, `address`, `email`, `heading`, `headingpic`, `headinglink`, `page`, `column1`, `column2`) VALUES
(1, '+8801673398900', 'Azimpur', 'pigeoninfinity@gmail.com', 'Highest Quality Pigeons for All', 'images/bg_1.jpg', '/Auction', 'home', 'null', 'null');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `phone` varchar(255) CHARACTER SET utf8 NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 NOT NULL,
  `address` varchar(255) CHARACTER SET utf8 NOT NULL,
  `bid_limit` int(11) NOT NULL DEFAULT 50000,
  `bid_point` int(11) NOT NULL DEFAULT 0,
  `total_bid_amount` int(11) NOT NULL DEFAULT 0,
  `facebook` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `last_login` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT current_timestamp(),
  `register_date` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT current_timestamp(),
  `dob` varchar(255) CHARACTER SET utf8 NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT 'UNVERIFIED',
  `nid` varchar(255) CHARACTER SET utf8 NOT NULL,
  `ip_address` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `pro_pic` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `x` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `reference` varchar(255) CHARACTER SET utf8 NOT NULL,
  `approvedBy` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `name`, `phone`, `email`, `password`, `address`, `bid_limit`, `bid_point`, `total_bid_amount`, `facebook`, `last_login`, `register_date`, `dob`, `status`, `nid`, `ip_address`, `pro_pic`, `x`, `reference`, `approvedBy`) VALUES
(1, 'asd', '+21234567812', 'asdad@asdasd', '7815696ecbf1c96e6894b779456d330e', 'asd', 50000, 0, 0, NULL, '2020-07-11 01:09:19', '11-07-2020', '2020-06-29', 'VERIFIED', 'asd', NULL, NULL, NULL, '', 'Xian'),
(2, 'Abir Hossain Xian', '01673398900', 'ahx.agent007@gmail.com', '25f9e794323b453885f5181f1b624d0b', 'Azimpur', 56600, 3, 33000, NULL, '2020-07-11 01:15:36', '11-07-2020', '2020-07-11', 'VERIFIED', '321654987', NULL, '2.jpg', NULL, '', 'Xian'),
(3, 'Jaber Hasan', '12345678911', 'abcd@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', 'USA', 50000, 0, 0, NULL, '2020-08-13 23:49:39', '2020-08-13 23:49:39', '2020-08-02', 'UNVERIFIED', '123456789', NULL, NULL, NULL, '', ''),
(4, 'asd', '12345678910', 'asd@asd.com', '7815696ecbf1c96e6894b779456d330e', 'asd', 50000, 0, 0, NULL, '2020-08-15 01:51:49', '2020-08-15 01:51:49', '2020-07-28', 'UNVERIFIED', 'asd', NULL, NULL, NULL, '', 'Xian'),
(5, 'asd3', '12365478932', 'asd3@asd3', '6867d9167683fb8f42558a81ad107f5b', 'asd3as', 50000, 0, 0, NULL, '2020-08-15 01:54:45', '2020-08-15 01:54:45', '2020-08-26', 'UNVERIFIED', 'asd3', NULL, NULL, NULL, 'asd2', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auctionevent`
--
ALTER TABLE `auctionevent`
  ADD PRIMARY KEY (`AuctionID`);

--
-- Indexes for table `bid`
--
ALTER TABLE `bid`
  ADD PRIMARY KEY (`BidID`);

--
-- Indexes for table `highfancier`
--
ALTER TABLE `highfancier`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pigeon`
--
ALTER TABLE `pigeon`
  ADD PRIMARY KEY (`PigeonID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auctionevent`
--
ALTER TABLE `auctionevent`
  MODIFY `AuctionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `bid`
--
ALTER TABLE `bid`
  MODIFY `BidID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `highfancier`
--
ALTER TABLE `highfancier`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pigeon`
--
ALTER TABLE `pigeon`
  MODIFY `PigeonID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
