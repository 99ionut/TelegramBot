-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2020 at 12:49 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `telegrambot`
--

-- --------------------------------------------------------

--
-- Table structure for table `adcampaign`
--

CREATE TABLE `adcampaign` (
  `campaignId` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `description` text NOT NULL,
  `nsfw` tinyint(1) NOT NULL,
  `clicks` int(11) NOT NULL,
  `cpc` float NOT NULL,
  `dailyBudget` float NOT NULL,
  `status` tinyint(1) NOT NULL,
  `url` varchar(512) NOT NULL,
  `username` varchar(128) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `totalclicks` int(11) NOT NULL,
  `seconds` int(11) NOT NULL,
  `dateAdded` date DEFAULT NULL,
  `speed` varchar(20) NOT NULL,
  `reports` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adcampaign`
--

INSERT INTO `adcampaign` (`campaignId`, `title`, `description`, `nsfw`, `clicks`, `cpc`, `dailyBudget`, `status`, `url`, `username`, `country`, `totalclicks`, `seconds`, `dateAdded`, `speed`, `reports`) VALUES
(89, 'wwwwwwwwww', 'eeeeeeeeeeeeee', 1, 0, 0.16, 73, 1, 'http://facebook.com', 'IonutZuZu', 'us,de,gb,fr,it,ru,', 0, 10, '2020-12-06', 'faster', 0),
(90, 'wwwwwwwwwww', 'yyyyyyyyyyyyyyyy', 1, 0, 0.1467, 2934, 1, 'http://facebook.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 0),
(91, 'wwwwwwwwwwww', 'ttttttttttttttttt', 1, 0, 0.147, 588, 1, 'http://facebook.com', 'IonutZuZu', 'us,de,gb,fr,jp,ch,my,', 0, 10, '2020-12-06', 'faster', 0),
(92, 'ssssssssss', 'fffffffffffffff', 1, 0, 0.0294, 2941, 1, 'http://youtube.com', 'IonutZuZu', 'gb,fr,', 0, 10, '2020-12-06', 'slowest', 0),
(93, 'ssssssssssssss', 'rrrrrrrrrrrrrrrrrrrrr', 0, 0, 0.441, 2941, 1, 'http://twitch.tv', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'faster', 0),
(94, 'oooooooooooo', 'ppppppppppppppppp', 0, 0, 0.441, 1471, 1, 'http://wwwwwwwwwww.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'faster', 0),
(95, 'ooooooooooooo', 'ppppppppppppppp', 0, 0, 0.1471, 2942, 1, 'http://xxxxxxxxxxx.com', 'IonutZuZu', 'gb,fr,', 0, 58, '2020-12-06', 'faster', 0),
(96, 'sssssssss', 'uuuuuuuuuuuuuuuu', 1, 0, 0.4413, 2942, 1, 'http://reddit.com', 'IonutZuZu', 'us,', 0, 10, '2020-12-06', 'fastest', 0),
(97, 'wwwwwwwwwwwwww', 'eeeeeeeeeeeeeeee', 1, 0, 0.0293, 1465, 1, 'http://omega.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 0),
(98, 'wwwwwwwwwwwww', 'kkkkkkkkkkkkkkkkkkk', 0, 0, 0.4405, 2936, 1, 'http://yyyyyyyy.com', 'IonutZuZu', 'xx', 0, 23, '2020-12-06', 'fastest', 0),
(99, 'wwwwwww', 'ggggggggggggg', 0, 0, 0.0293, 73, 1, 'http://youtube.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 0),
(100, 'wwwwwwwwww', 'eeeeeeeeeeeee', 0, 0, 0.1468, 587, 1, 'http://uuuuuuuuuuuu.com', 'IonutZuZu', 'xx', 0, 15, '2020-12-06', 'faster', 0),
(101, 'wwwwwwwwww', 'eeeeeeeeeeeee', 0, 0, 0.4405, 1468, 1, 'http://pppppppp.com', 'IonutZuZu', 'xx', 0, 25, '2020-12-06', 'fastest', 0),
(102, 'ssssssssssss', 'wwwwwwwwwww', 0, 0, 0.0293, 1469, 1, 'http://ooo.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 0),
(103, 'sssssssss', 'ttttttttttt', 1, 0, 0.0293, 2939, 1, 'http://ooo.com', 'IonutZuZu', 'xx', 0, 30, '2020-12-06', 'slowest', 0),
(104, 'sssssssssss', 'sssssssssssssssssssss', 1, 0, 0.0299, 2998, 1, 'http://sssssssss.com', 'IonutZuZu', 'us,de,', 0, 10, '2020-12-07', 'slowest', 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` varchar(64) NOT NULL,
  `referral` varchar(64) NOT NULL,
  `taskAlert` tinyint(1) NOT NULL,
  `seeNsfw` tinyint(1) NOT NULL,
  `address` varchar(64) NOT NULL,
  `referredBy` varchar(64) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `username` varchar(128) NOT NULL,
  `dateJoined` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `referral`, `taskAlert`, `seeNsfw`, `address`, `referredBy`, `country`, `username`, `dateJoined`) VALUES
('626602519', 'bPEKnEKO', 1, 0, '2N5ApERYxn2mWiK584KEb3Y6qZtX9n8YHKp', '', 'en', 'IonutZuZu', NULL),
('374408239', 'LdWxuVuw', 1, 1, '2My1b62H5U4uQiYZvd8nXDt1rxdcQUnzGre', '', 'de', 'Trafficbossadmin', NULL),
('666666', 'eeeeee', 1, 1, 'wwwwwwwww', 'wwwwwwwww', 'ww', 'wwwwwww', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD PRIMARY KEY (`campaignId`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`) USING BTREE,
  ADD UNIQUE KEY `address` (`address`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adcampaign`
--
ALTER TABLE `adcampaign`
  MODIFY `campaignId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD CONSTRAINT `adcampaign_ibfk_2` FOREIGN KEY (`username`) REFERENCES `user` (`username`),
  ADD CONSTRAINT `adcampaign_ibfk_3` FOREIGN KEY (`username`) REFERENCES `user` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
