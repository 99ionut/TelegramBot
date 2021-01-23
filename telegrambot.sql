-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 23, 2021 at 12:43 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.3.25

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
  `reports` int(11) NOT NULL DEFAULT 0,
  `dailyBudgetSpent` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adcampaign`
--

INSERT INTO `adcampaign` (`campaignId`, `title`, `description`, `nsfw`, `clicks`, `cpc`, `dailyBudget`, `status`, `url`, `username`, `country`, `totalclicks`, `seconds`, `dateAdded`, `speed`, `reports`, `dailyBudgetSpent`) VALUES
(92, 'ssssssssss', 'fffffffffffffff', 1, 0, 0.0294, 2941, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'gb,fr,', 0, -1, '2020-12-06', 'slowest', 0, 0),
(93, 'ssssssssssssss', 'rrrrrrrrrrrrrrrrrrrrr', 0, 0, 0.441, 2941, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, -1, '2020-12-06', 'faster', 0, 0),
(94, 'oooooooooooo', 'ppppppppppppppppp', 0, 0, 0.441, 1471, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, -1, '2020-12-06', 'faster', 0, 0),
(95, 'ooooooooooooo', 'ppppppppppppppp', 0, 0, 0.1471, 2942, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'gb,fr,', 0, 58, '2020-12-06', 'faster', 0, 0),
(100, 'ppppppppp', 'eeeeeeeeeeeee', 0, 1, 0.1468, 587, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, 3, '2020-12-06', 'faster', 0, 0.2936),
(108, 'rrrrrrrrrr', 'rrrrrrrrrr', 0, 4, 43, 444, 1, 'https://ltcminer.com/42', 'wwwwwww', 'de', 1, 22, '2020-12-03', 'slow', 0, 0),
(109, 'ffffSO GRATISSSS', 'ffin f', 1, 0, 0.0221, 1106, 1, 'https://ltcminer.com/42', 'cikamoto', 'xx', 0, -1, '2020-12-26', 'slowest', 0, 0),
(110, '😳😳😳ds😳😳😳😳', '🤡🤡🤡🤡 ild', 1, 0, 0.3318, 1106, 1, 'https://ltcminer.com/42', 'cikamoto', 'xx', 0, -1, '2020-12-26', 'fastest', 0, 0),
(112, 'status try', 'statusssssstry', 0, 0, 0.061, 1221, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, -1, '2021-01-12', 'faster', 0, 0),
(113, '5555555555', '55555555555555555555', 0, 0, 0.1613, 1075, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, -1, '2021-01-16', 'fastest', 0, 0),
(114, 'ssssssssssssss', 'ddddddddddddddddd', 0, 0, 0.1613, 1075, 1, 'https://www.twitch.tv', 'IonutZuZu', 'xx', 0, -1, '2021-01-16', 'fastest', 0, 0),
(115, 'wwwwwwwwwwwwwwww', 'wwwwwwwwwwwwwwwwwwwww', 0, 0, 0.1613, 1075, 1, 'https://ltcminer.com/42', 'IonutZuZu', 'xx', 0, 22, '2021-01-16', 'fastest', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('ciao', 'ciao');

-- --------------------------------------------------------

--
-- Table structure for table `country`
--

CREATE TABLE `country` (
  `code` varchar(5) NOT NULL,
  `country` varchar(30) DEFAULT NULL,
  `clicks` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `country`
--

INSERT INTO `country` (`code`, `country`, `clicks`) VALUES
('ae', 'United Arab Emirates	', 0),
('af', 'Afghanistan', 0),
('al', 'Albania', 0),
('am', 'Armenia', 0),
('ao', 'Angola', 0),
('ar', 'Argentina', 0),
('at', 'Austria', 0),
('au', 'Australia	', 0),
('az', 'Azerbaijan', 0),
('ba', 'Bosnia and Herzegovina	', 0),
('bb', 'Barbados', 4),
('bd', 'Bangladesh', 0),
('be', 'Belgium', 0),
('bf', 'Burkina Faso	', 0),
('bg', 'Bulgaria', 0),
('bh', 'Bahrain', 0),
('bi', 'Burundi', 0),
('bj', 'Benin', 0),
('bn', 'Brunei	', 0),
('bo', 'Bolivia', 12),
('br', 'Brazil', 0),
('bw', 'Botswana', 0),
('by', 'Belarus', 0),
('ca', 'Canada', 0),
('cd', 'Congo', 0),
('cg', 'Republic of the Congo	', 0),
('ch', 'Switzerland', 0),
('ci', 'Ivory Coast	', 0),
('cl', 'Chile', 0),
('cm', 'Cameroon', 0),
('cn', 'China', 0),
('co', 'Colombia', 0),
('cr', 'Costa Rica	', 0),
('cu', 'Cuba', 0),
('cv', 'Cabo Verde	', 0),
('cy', 'Cyprus', 0),
('cz', 'Czech Republic	', 0),
('de', 'Germany', 0),
('dk', 'Denmark', 0),
('do', 'Dominican Republic	', 0),
('dz', 'Algeria', 0),
('ec', 'Ecuador', 0),
('ee', 'Estonia', 0),
('eg', 'Egypt', 0),
('en', 'English', 0),
('er', 'Eritrea', 0),
('es', 'Spain', 0),
('et', 'Ethiopia', 0),
('fi', 'Finland', 0),
('fj', 'Fiji	', 0),
('fr', 'France', 665),
('ga', 'Gabon', 0),
('gb', 'United Kingdom	', 0),
('gd', 'Grenada', 0),
('ge', 'Georgia', 0),
('gh', 'Ghana', 0),
('gi', 'Gibraltar', 0),
('gn', 'Guinea', 111),
('gr', 'Greece', 0),
('gt', 'Guatemala', 0),
('hk', 'Hong Kong	', 0),
('hn', 'Honduras', 0),
('hr', 'Croatia', 0),
('ht', 'Haiti', 0),
('hu', 'Hungary', 0),
('id', 'Indonesia', 0),
('ie', 'Ireland', 0),
('il', 'Israel', 0),
('in', 'India', 0),
('iq', 'Iraq', 0),
('ir', 'Iran', 0),
('is', 'Iceland', 444),
('it', 'Italy', 0),
('jm', 'Jamaica', 0),
('jo', 'Hashemite Kingdom of Jordan	', 0),
('jp', 'Japan', 0),
('ke', 'Kenya', 0),
('kg', 'Kyrgyzstan', 0),
('kh', 'Cambodia', 0),
('kr', 'Republic of Korea	', 0),
('kw', 'Kuwait', 0),
('ky', 'Kyrgyzstan', 0),
('kz', 'Kazakhstan', 0),
('la', 'Laos', 0),
('lb', 'Lebanon', 0),
('lk', 'Sri Lanka	', 0),
('lr', 'Liberia', 0),
('ls', 'Republic of Lithuania	', 0),
('lt', 'Republic of Lithuania	', 0),
('lu', 'Luxembourg', 0),
('lv', 'Latvia', 0),
('ly', 'Libya', 0),
('ma', 'Morocco', 0),
('md', 'Republic of Moldova	', 0),
('me', 'Montenegro', 0),
('mg', 'Madagascar', 0),
('mk', 'Macedonia', 0),
('ml', 'Mali', 0),
('mm', 'Myanmar', 0),
('mn', 'Mongolia', 0),
('mp', 'Northern Mariana Islands	', 0),
('mt', 'Malta', 0),
('mu', 'Mauritius', 0),
('mv', 'Maldives', 0),
('mw', 'Malawi', 0),
('mx', 'Mexico', 0),
('my', 'Malaysia', 0),
('mz', 'Mozambique', 0),
('nc', 'New Caledonia	', 0),
('ne', 'Niger', 0),
('ng', 'Nigeria', 0),
('ni', 'Nicaragua', 0),
('nl', 'Netherlands', 0),
('no', 'Norway', 0),
('np', 'Nepal', 0),
('nz', 'New Zealand	', 0),
('om', 'Oman', 0),
('pa', 'Panama', 0),
('pe', 'Peru', 0),
('pf', 'French Polynesia	', 0),
('pg', 'Papua New Guinea	', 0),
('ph', 'Philippines', 0),
('pk', 'Pakistan', 0),
('pl', 'Poland', 0),
('pr', 'Puerto Rico	', 0),
('ps', 'Palestine', 0),
('pt', 'Portugal', 0),
('py', 'Paraguay', 0),
('qa', 'Qatar', 0),
('ro', 'Romania', 0),
('rs', 'Serbia', 0),
('ru', 'Russia', 0),
('rw', 'Rwanda', 0),
('sc', 'Seychelles', 0),
('sd', 'Sudan', 0),
('se', 'Sweden', 0),
('sg', 'Singapore', 0),
('si', 'Slovenia', 0),
('sk', 'Slovakia', 0),
('sl', 'Sierra Leone	', 0),
('sm', 'San Marino	', 0),
('sn', 'Senegal', 0),
('so', 'Somalia	', 0),
('sr', 'Suriname', 0),
('sy', 'Syria', 0),
('sz', 'Eswatini', 0),
('tc', 'Turks and Caicos Islands	', 0),
('tg', 'Togo', 0),
('th', 'Thailand', 0),
('tj', 'Tajikistan', 0),
('tn', 'Tunisia', 0),
('to', 'Tonga', 0),
('tr', 'Turkey', 0),
('tt', 'Trinidad and Tobago	', 0),
('tw', 'Taiwan', 0),
('tz', 'Tanzania', 0),
('ua', 'Ukraine', 0),
('ug', 'Uganda', 0),
('us', 'United States	', 0),
('uy', 'Uruguay', 0),
('uz', 'Uzbekistan', 0),
('vc', 'Saint V and the Grenadines	', 0),
('ve', 'Venezuela', 0),
('vn', 'Vietnam', 0),
('xk', 'Kosovo', 0),
('xx', 'none', 0),
('ye', 'Yemen', 0),
('za', 'South Africa	', 0),
('zm', 'Zambia', 0),
('zw', 'Zimbabwe', 323);

-- --------------------------------------------------------

--
-- Table structure for table `link`
--

CREATE TABLE `link` (
  `customLink` varchar(64) NOT NULL,
  `username` varchar(128) NOT NULL,
  `campaignId` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `link`
--

INSERT INTO `link` (`customLink`, `username`, `campaignId`) VALUES
('251230050650', 'IonutZuZu', '100');

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `webhook` varchar(256) DEFAULT NULL,
  `blockIoApi` varchar(100) NOT NULL DEFAULT '',
  `blockIoSecretPin` varchar(256) NOT NULL,
  `blockIoVersion` varchar(10) NOT NULL,
  `minDepositAmount` varchar(100) NOT NULL,
  `minWithdrawAmount` varchar(100) NOT NULL,
  `botToken` varchar(150) NOT NULL,
  `mainAccount` varchar(256) NOT NULL,
  `ownerTake` float NOT NULL DEFAULT 1,
  `webhookWebsite` varchar(256) NOT NULL,
  `referralTake` float NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`webhook`, `blockIoApi`, `blockIoSecretPin`, `blockIoVersion`, `minDepositAmount`, `minWithdrawAmount`, `botToken`, `mainAccount`, `ownerTake`, `webhookWebsite`, `referralTake`) VALUES
('http://911514092064.ngrok.io/webhook', '8383-cae2-01f4-720f', 'telegrambot', '2', '1', '4', '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk', '2N1fJnGvvbLexRusQXet77fFAgoL6MuMRDx', 15, 'http://911514092064.ngrok.io/website', 1);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `id` int(11) NOT NULL,
  `transaction` varchar(256) NOT NULL,
  `amount` varchar(256) NOT NULL,
  `userAddress` varchar(256) NOT NULL,
  `userUsername` varchar(256) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`id`, `transaction`, `amount`, `userAddress`, `userUsername`, `date`) VALUES
(1, '36a64d7a29c0a7c4e8596c44b871f09ae98a986653023d5669596bfcd0757f03', '2.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 21:55:24'),
(2, '8928f211e45563e58187d61e187d849c85b3863e7ac3081567a933a97376c706', '3.12', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 21:57:32'),
(3, '8b7bbfbaba1ff188436fc653b115730c4ac96c29bb6e9f000184c6e82d2f80b0', '2.32', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 21:58:51'),
(4, '43acb23ac472cb8ba0e5d415fc47fcc8b346beea9ec48a9c1461fb7d1b1dcb99', '3.777', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 21:58:51'),
(5, 'd9764ab3d72d6c031ddb93cdee4a5bb4fcbfeed73cdc6798986670cef5ba365f', '3.21', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 22:26:10'),
(6, '0cdf357e86293548f91e3f07a3a45c22a7200c081377d7b9e4f41ce501ff6ab2', '6.79', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-06 22:27:32'),
(7, '28038aeeb6771fef96df9502325f9d2222eec3294b6228fc51fe67d283127cec', '3.92', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:35:27'),
(8, '04bf71f61caf40b24d21bd761fa90700ecccc210c41634eb72258017ac1d641c', '3.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:35:29'),
(9, '58373006aa1575a53303799b1e0ac340e16d66d62839c42131d6f50b2ca59766', '5.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:37:29'),
(10, '40c9911396687d13cd2e3ea9fb03baa5a822002863b02a187fb41c80cffedb08', '4.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:38:07'),
(11, '2fadf2063bb94a41ea452af71700dd12548782e573ebc71c9bab5d124dcec334', '6.23', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:53:48'),
(12, '12de445da55ff48844cbc1f7839fa6bdbb39e469a3e95ab6c42ad61de677585e', '3.77', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:53:49'),
(13, 'feaca75f14df8b744f96629e32c50f13e141cbdb456e17863b4bca323b7cd849', '5.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:53:52'),
(14, 'a32942328f6c523a6447980ea9773325d9be0ab64d0ffb314e99957b2f54e82b', '5.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:55:35'),
(15, '4ce3b2eb33b2a7a2cad9a1c2686f9cbdd23fb146e1ac9964d95659055a687cf2', '4.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:56:44'),
(16, '693b307c169447d4a2f52e6584774c9f286280bcbdc9a0a5d2367dd8de84656a', '4.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 15:59:14'),
(17, '17349091ee64ed2514a4aa6fb2e991c643263a79be123db40166840a54e04426', '4.0', '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', 'IonutZuZu', '2021-01-17 16:08:22');

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
  `dateJoined` date DEFAULT NULL,
  `virtualBalance` float NOT NULL DEFAULT 0,
  `lastAd` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `referral`, `taskAlert`, `seeNsfw`, `address`, `referredBy`, `country`, `username`, `dateJoined`, `virtualBalance`, `lastAd`) VALUES
('302035126', 'XmPAksry', 1, 1, '2N3pp5phiP5qADTh9E8TEKJYmsv5Pt1WfeS', 'IonutZuZu', 'it', 'Arcadell', '2020-12-27', 122, -1),
('286847584', 'fqpEXDli', 1, 1, '2MwjSr1r1gsUTNN5pJGTNkTZDh9FSrkJK5A', '', 'it', 'cikamoto', '2020-12-26', 40, -1),
('default', '', 1, 1, '2N1fJnGvvbLexRusQXet77fFAgoL6MuMRDx', '', 'en', 'default', '2021-01-03', 472.99, -1),
('626602519', 'bPEKnEKO', 1, 1, '2N9DqycM4VedDzM5cJdHD7hARhxQEZM77Wd', '', 'en', 'IonutZuZu', NULL, 1207.8, 100),
('oppolo', '', 1, 1, '2N22GhmvbrhfCJv9exKHJ7Gvb5L8qu2H2vE', '', 'uk', 'oppolo', '2020-12-09', 2, -1),
('test', 'wwww', 1, 1, '2N3YcfGc3ozvgUUkZgMQmpjzBVuofChhiLi', '', 'de', 'test', '2020-12-01', 33, -1),
('374408239', 'LdWxuVuw', 1, 1, '2My1b62H5U4uQiYZvd8nXDt1rxdcQUnzGre', '', 'de', 'Trafficbossadmin', NULL, 4, -1),
('666666', 'eeeeee', 1, 1, 'wwwwwwwww', 'wwwwwwwww', 'ww', 'wwwwwww', NULL, 5, -1);

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
-- Indexes for table `country`
--
ALTER TABLE `country`
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `link`
--
ALTER TABLE `link`
  ADD PRIMARY KEY (`customLink`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`botToken`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `campaignId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=116;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

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
