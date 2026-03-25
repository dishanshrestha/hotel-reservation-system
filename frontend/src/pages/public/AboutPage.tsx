import { Users, Award, Coffee, Clock } from 'lucide-react';

const stats = [
  { icon: Users, label: 'Happy Guests', value: '5,000+' },
  { icon: Award, label: 'Awards Won', value: '25+' },
  { icon: Coffee, label: 'Rooms Available', value: '120' },
  { icon: Clock, label: 'Years Experience', value: '15+' },
];

export default function AboutPage() {
  return (
    <div>
      {/* Header */}
      <section className="bg-brand-dark py-16 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">About Us</h1>
        <p className="text-gray-300">Learn more about our hotel and services</p>
      </section>

      {/* Main Content */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-brand-ink mb-2">Welcome to StarterHotel, Kathmandu</h2>
              <div className="w-16 h-1 bg-brand-gold mb-6" />
              <p className="text-gray-600 mb-4 leading-relaxed">
                Nestled in the heart of Thamel, Kathmandu&apos;s most vibrant neighborhood, StarterHotel
                blends traditional Nepali hospitality with modern comfort. Just steps from ancient temples,
                bustling bazaars, and the gateway to the Himalayas, our hotel has welcomed travelers from
                around the world since its founding.
              </p>
              <p className="text-gray-600 mb-4 leading-relaxed">
                Our rooms are designed with locally sourced Newari woodwork, handwoven Dhaka textiles,
                and modern amenities to create a uniquely Nepali experience. From our rooftop terrace,
                guests can enjoy panoramic views of the Kathmandu Valley and the snow-capped Himalayan range.
              </p>
              <p className="text-gray-600 leading-relaxed">
                Whether you&apos;re preparing for an Everest Base Camp trek, exploring Kathmandu&apos;s
                UNESCO World Heritage Sites, or simply seeking a peaceful retreat, StarterHotel is your
                perfect home base in Nepal.
              </p>
            </div>
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80"
                alt="About StarterHotel"
                className="rounded-lg shadow-lg w-full object-cover h-[450px]"
              />
              <div className="absolute -bottom-6 -left-6 bg-brand-gold text-brand-dark p-6 rounded-lg shadow-lg hidden md:block">
                <p className="text-3xl font-bold">15+</p>
                <p className="text-sm font-medium">Years of Excellence</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 bg-brand-primary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <stat.icon size={36} className="text-brand-gold mx-auto mb-3" />
                <p className="text-3xl font-bold text-white">{stat.value}</p>
                <p className="text-sm text-teal-100 mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-10">
            <div className="bg-white p-8 rounded-lg shadow-sm">
              <h3 className="text-2xl font-bold text-brand-ink mb-4">Our Mission</h3>
              <div className="w-12 h-1 bg-brand-gold mb-4" />
              <p className="text-gray-600 leading-relaxed">
                To provide exceptional hospitality experiences that exceed our guests&apos; expectations,
                creating lasting memories through personalized service, world-class amenities, and an
                unwavering commitment to quality and comfort.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-sm">
              <h3 className="text-2xl font-bold text-brand-ink mb-4">Our Vision</h3>
              <div className="w-12 h-1 bg-brand-gold mb-4" />
              <p className="text-gray-600 leading-relaxed">
                To be recognized as a leading destination for travelers seeking an extraordinary blend of
                luxury, comfort, and authentic hospitality. We aim to set new standards in the hospitality
                industry through innovation and dedication to our guests.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
